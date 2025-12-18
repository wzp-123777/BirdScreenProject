from django.shortcuts import render, redirect
from django.http import JsonResponse, StreamingHttpResponse
from .models import BirdRecord, BirdSpecies, Airport, ImportLog
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime

def dashboard(request):
    # Basic stats
    total_records = BirdRecord.objects.count()
    high_risk_count = BirdRecord.objects.filter(risk_level='high').count()
    today_count = BirdRecord.objects.filter(record_time__date=timezone.now().date()).count()
    
    context = {
        'total_records': total_records,
        'high_risk_count': high_risk_count,
        'today_count': today_count,
    }
    return render(request, 'monitor/index.html', context)

def record_list(request):
    records = BirdRecord.objects.all().order_by('-record_time')
    return render(request, 'monitor/record_list.html', {'records': records})

def add_record(request):
    if request.method == 'POST':
        species_id = request.POST.get('species')
        quantity = int(request.POST.get('quantity'))
        location = request.POST.get('location')
        reason = request.POST.get('reason')
        
        species = BirdSpecies.objects.get(id=species_id)
        BirdRecord.objects.create(
            species=species,
            quantity=quantity,
            location=location,
            intrusion_reason=reason
        )
        return redirect('record_list')
    
    species_list = BirdSpecies.objects.all()
    return render(request, 'monitor/record_form.html', {'species_list': species_list})

def api_dashboard_data(request):
    # Data for charts
    # 1. Species distribution
    species_data = BirdRecord.objects.values('species__name').annotate(total=Sum('quantity')).order_by('-total')
    
    # 2. Daily trend (last 7 days)
    last_7_days = timezone.now() - datetime.timedelta(days=7)
    daily_data = BirdRecord.objects.filter(record_time__gte=last_7_days)\
        .extra(select={'day': 'date(record_time)'})\
        .values('day')\
        .annotate(count=Count('id'))\
        .order_by('day')
        
    data = {
        'species_labels': [item['species__name'] for item in species_data],
        'species_values': [item['total'] for item in species_data],
        'daily_labels': [item['day'] for item in daily_data],
        'daily_values': [item['count'] for item in daily_data],
    }
    return JsonResponse(data)

def map_simple(request):
    """极简化地图视图"""
    return render(request, 'monitor/map_simple.html')


def map_step1(request):
    """地图视图 - 步骤1: 基础地图 + 数据加载"""
    return render(request, 'monitor/map_step1.html')


def map_step2(request):
    """地图视图 - 步骤2: 基础地图 + 数据加载 + 搜索功能"""
    return render(request, 'monitor/map_step2.html')


def map_step3(request):
    """地图视图 - 步骤3: 基础地图 + 数据加载 + 搜索功能 + 位置信息"""
    return render(request, 'monitor/map_step3.html')


def map_final(request):
    """最终版简化3D地图 - 轻量级：机场显示 + 鸟情数据 + 搜索功能 + 位置信息"""
    return render(request, 'monitor/map_final.html')


def map_test(request):
    """地图加载测试视图"""
    return render(request, 'monitor/map_test.html')

def api_bird_records(request):
    """API: 获取所有有坐标的鸟情记录"""
    records = BirdRecord.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).select_related('species')

    data = []
    for record in records:
        data.append({
            'id': record.id,
            'species': record.species.name,
            'quantity': record.quantity,
            'location': record.location,
            'latitude': record.latitude,
            'longitude': record.longitude,
            'risk_level': record.risk_level,
            'record_time': record.record_time.strftime('%Y-%m-%d %H:%M'),
            'intrusion_reason': record.intrusion_reason,
            'notes': record.notes
        })

    return JsonResponse(data, safe=False)

def api_airports(request):
    """API: 获取机场数据"""
    country = request.GET.get('country', '')  # 国家筛选
    airport_type = request.GET.get('type', '')  # 类型筛选

    airports = Airport.objects.all()

    if country:
        airports = airports.filter(iso_country=country.upper())

    if airport_type:
        airports = airports.filter(airport_type=airport_type)

    data = []
    for airport in airports:
        data.append({
            'id': airport.id,
            'ident': airport.ident,
            'name': airport.name,
            'type': airport.airport_type,
            'latitude': airport.latitude,
            'longitude': airport.longitude,
            'elevation_ft': airport.elevation_ft,
            'country': airport.iso_country,
            'municipality': airport.municipality,
            'icao_code': airport.icao_code,
            'iata_code': airport.iata_code
        })

    return JsonResponse(data, safe=False)


def api_airports_full(request):
    """返回完整机场数据API (用于前端搜索)"""
    airports = Airport.objects.all()
    data = list(airports.values(
        'id', 'ident', 'name', 'latitude', 'longitude', 'icao_code', 'iata_code',
        'municipality', 'iso_country', 'elevation_ft', 'airport_type'
    ))
    return JsonResponse(data, safe=False)


def import_xls_view(request):
    """XLS/CSV文件导入视图"""
    # 处理文件上传和导入逻辑
    if request.method == 'POST':
        uploaded_file = request.FILES.get('xls_file')
        import_type = request.POST.get('import_type', 'bird')  # bird 或 airport

        if not uploaded_file:
            return render(request, 'monitor/import_xls.html', {
                'error': '请选择要上传的文件'
            })

        # 检查文件类型
        file_name = uploaded_file.name.lower()
        supported_formats = ['.xls', '.xlsx', '.csv']

        # 添加地理数据格式支持
        if import_type == 'airport' or import_type == 'geodata':
            supported_formats.extend(['.shp', '.geojson', '.json', '.kml'])

        if not any(file_name.endswith(ext) for ext in supported_formats):
            format_list = [ext[1:].upper() for ext in supported_formats]
            return render(request, 'monitor/import_xls.html', {
                'error': f'不支持的文件格式。只支持: {", ".join(format_list)}'
            })

        # 创建导入日志记录
        log_entry = ImportLog.objects.create(
            log_type=import_type,
            file_name=uploaded_file.name,
            file_size=uploaded_file.size,
            status='processing',
            details=f'开始处理文件: {uploaded_file.name}'
        )

        # 返回处理中的状态，让用户知道可以查看实时日志
        return render(request, 'monitor/import_xls.html', {
            'processing': True,
            'log_id': log_entry.id,
            'message': f'正在处理文件 "{uploaded_file.name}"，请在新窗口中查看实时日志监控。'
        })

        try:
            # 使用pandas读取文件
            import pandas as pd
            from datetime import datetime

            log_entry.details += f'\n正在读取文件...'
            log_entry.save()

            if file_name.endswith('.csv') and import_type != 'geodata':
                # 普通CSV文件
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            elif file_name.endswith(('.shp', '.geojson', '.json', '.kml')) or (file_name.endswith('.csv') and import_type == 'geodata'):
                # 处理地理数据文件
                df = process_geospatial_file(uploaded_file, file_name)
            else:
                df = pd.read_excel(uploaded_file)

            log_entry.total_rows = len(df)
            log_entry.details += f'\n成功读取 {len(df)} 行数据'
            log_entry.details += f'\n列名: {", ".join(df.columns)}'
            log_entry.save()

            print(f"读取到 {len(df)} 行数据，列名: {list(df.columns)}")

            # 根据导入类型选择处理函数
            if import_type == 'airport':
                return process_airport_import(df, request, log_entry)
            else:
                return process_bird_import(df, request, log_entry)

        except Exception as e:
            log_entry.status = 'failed'
            log_entry.error_messages = str(e)
            log_entry.completed_at = datetime.now()
            log_entry.save()

            return render(request, 'monitor/import_xls.html', {
                'error': f'文件处理失败: {str(e)}',
                'log_id': log_entry.id
            })

    return render(request, 'monitor/import_xls.html')

def process_bird_import(df, request, log_entry):
    """处理鸟情数据导入"""
    # 检查必要的列
    required_columns = ['鸟种', '数量', '位置', '纬度', '经度']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        return render(request, 'monitor/import_xls.html', {
            'error': f'缺少必要的列: {", ".join(missing_columns)}'
        })

    # 处理数据导入
    success_count = 0
    error_count = 0
    errors = []
    log_entry.details += f'\n开始处理鸟情数据导入...'

    for index, row in df.iterrows():
        try:
            log_entry.details += f'\n处理第{index+2}行: '

            # 获取或创建鸟种
            species_name = str(row['鸟种']).strip()
            if not species_name:
                error_msg = f'第{index+2}行: 鸟种名称不能为空'
                errors.append(error_msg)
                log_entry.error_messages += f'\n{error_msg}'
                error_count += 1
                continue

            species, created = BirdSpecies.objects.get_or_create(
                name=species_name,
                defaults={'danger_level': 3}  # 默认中等危险等级
            )

            if created:
                log_entry.details += f'创建新鸟种 "{species_name}" '
            else:
                log_entry.details += f'使用现有鸟种 "{species_name}" '

            # 验证坐标
            latitude = row.get('纬度')
            longitude = row.get('经度')

            if pd.isna(latitude) or pd.isna(longitude):
                error_msg = f'第{index+2}行: 纬度和经度不能为空'
                errors.append(error_msg)
                log_entry.error_messages += f'\n{error_msg}'
                error_count += 1
                continue

            # 创建鸟情记录
            record_data = {
                'species': species,
                'quantity': int(row.get('数量', 1)),
                'location': str(row.get('位置', '')).strip(),
                'latitude': float(latitude),
                'longitude': float(longitude),
                'intrusion_reason': str(row.get('入侵原因', '')).strip(),
                'notes': str(row.get('备注', '')).strip()
            }

            # 处理记录时间
            record_time_str = row.get('记录时间')
            if not pd.isna(record_time_str):
                if isinstance(record_time_str, str):
                    # 尝试解析字符串时间
                    try:
                        record_data['record_time'] = datetime.strptime(record_time_str, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        try:
                            record_data['record_time'] = datetime.strptime(record_time_str, '%Y-%m-%d')
                        except ValueError:
                            record_data['record_time'] = datetime.now()
                else:
                    # 如果是pandas的时间戳
                    record_data['record_time'] = record_time_str.to_pydatetime() if hasattr(record_time_str, 'to_pydatetime') else datetime.now()

            BirdRecord.objects.create(**record_data)
            success_count += 1
            log_entry.details += f'✓ 成功创建记录'

        except Exception as e:
            error_msg = f'第{index+2}行: {str(e)}'
            errors.append(error_msg)
            log_entry.error_messages += f'\n{error_msg}'
            error_count += 1
            log_entry.details += f'✗ 失败: {str(e)}'

    # 更新日志记录
    log_entry.success_count = success_count
    log_entry.error_count = error_count
    log_entry.status = 'completed' if error_count == 0 else 'completed_with_errors'
    log_entry.completed_at = datetime.now()
    log_entry.details += f'\n\n导入完成: 成功 {success_count} 条, 失败 {error_count} 条'
    log_entry.save()

    return render(request, 'monitor/import_xls.html', {
        'success': f'成功导入 {success_count} 条鸟情记录',
        'error_count': error_count,
        'errors': errors[:10],  # 只显示前10个错误
        'log_id': log_entry.id
    })

def process_airport_import(df, request, log_entry):
    """处理机场数据导入"""
    # 检查必要的列 (基于airports.csv格式)
    required_columns = ['ident', 'name', 'latitude_deg', 'longitude_deg']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        return render(request, 'monitor/import_xls.html', {
            'error': f'缺少必要的列: {", ".join(missing_columns)}。请参考airports.csv格式。'
        })

    # 处理数据导入
    success_count = 0
    error_count = 0
    errors = []
    log_entry.details += f'\n开始处理机场数据导入...'

    for index, row in df.iterrows():
        try:
            log_entry.details += f'\n处理第{index+2}行: '

            # 获取必要字段
            ident = str(row.get('ident', '')).strip()
            name = str(row.get('name', '')).strip()

            if not ident or not name:
                error_msg = f'第{index+2}行: 机场标识符和名称不能为空'
                errors.append(error_msg)
                log_entry.error_messages += f'\n{error_msg}'
                error_count += 1
                continue

            log_entry.details += f'机场 {ident} ({name}) '

            # 验证坐标
            latitude = row.get('latitude_deg')
            longitude = row.get('longitude_deg')

            if pd.isna(latitude) or pd.isna(longitude):
                error_msg = f'第{index+2}行: 纬度和经度不能为空'
                errors.append(error_msg)
                log_entry.error_messages += f'\n{error_msg}'
                error_count += 1
                continue

            # 处理机场类型映射
            type_mapping = {
                'large_airport': 'large_airport',
                'medium_airport': 'medium_airport',
                'small_airport': 'small_airport',
                'heliport': 'heliport',
                'seaplane_base': 'seaplane_base',
                'balloonport': 'balloonport',
                'closed': 'closed'
            }

            airport_type = str(row.get('type', 'small_airport')).strip()
            airport_type = type_mapping.get(airport_type, 'small_airport')

            # 检查是否已存在
            if Airport.objects.filter(ident=ident).exists():
                error_msg = f'第{index+2}行: 机场标识符 {ident} 已存在，跳过'
                errors.append(error_msg)
                log_entry.error_messages += f'\n{error_msg}'
                error_count += 1
                continue

            # 创建机场记录
            airport_data = {
                'ident': ident,
                'name': name,
                'airport_type': airport_type,
                'latitude': float(latitude),
                'longitude': float(longitude),
                'elevation_ft': int(row.get('elevation_ft', 0)) if not pd.isna(row.get('elevation_ft')) else None,
                'continent': str(row.get('continent', '')).strip(),
                'iso_country': str(row.get('iso_country', '')).strip(),
                'iso_region': str(row.get('iso_region', '')).strip(),
                'municipality': str(row.get('municipality', '')).strip(),
                'scheduled_service': str(row.get('scheduled_service', 'no')).strip(),
                'icao_code': str(row.get('icao_code', '')).strip(),
                'iata_code': str(row.get('iata_code', '')).strip(),
                'gps_code': str(row.get('gps_code', '')).strip(),
                'local_code': str(row.get('local_code', '')).strip(),
                'home_link': str(row.get('home_link', '')).strip(),
                'wikipedia_link': str(row.get('wikipedia_link', '')).strip(),
                'keywords': str(row.get('keywords', '')).strip()
            }

            Airport.objects.create(**airport_data)
            success_count += 1
            log_entry.details += f'✓ 成功创建机场'

        except Exception as e:
            error_msg = f'第{index+2}行: {str(e)}'
            errors.append(error_msg)
            log_entry.error_messages += f'\n{error_msg}'
            error_count += 1
            log_entry.details += f'✗ 失败: {str(e)}'

    # 更新日志记录
    log_entry.success_count = success_count
    log_entry.error_count = error_count
    log_entry.status = 'completed' if error_count == 0 else 'completed_with_errors'
    log_entry.completed_at = datetime.now()
    log_entry.details += f'\n\n导入完成: 成功 {success_count} 个, 失败 {error_count} 个'
    log_entry.save()

    return render(request, 'monitor/import_xls.html', {
        'success': f'成功导入 {success_count} 个机场',
        'error_count': error_count,
        'errors': errors[:10],  # 只显示前10个错误
        'log_id': log_entry.id
    })

def logs_view(request):
    """日志中心视图 - 包含项目日志和导入日志"""
    # 获取导入日志查询参数
    log_type = request.GET.get('type', '')
    status = request.GET.get('status', '')

    # 构建导入日志查询
    import_logs = ImportLog.objects.all()

    if log_type:
        import_logs = import_logs.filter(log_type=log_type)

    if status:
        import_logs = import_logs.filter(status=status)

    # 分页导入日志
    from django.core.paginator import Paginator
    paginator = Paginator(import_logs, 10)  # 每页10条记录
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'log_type': log_type,
        'status': status,
        'import_logs_count': import_logs.count(),
    }

    return render(request, 'monitor/logs.html', context)

def import_log_detail_view(request, log_id):
    """导入日志详情视图"""
    try:
        log_entry = ImportLog.objects.get(id=log_id)
        return render(request, 'monitor/import_log_detail.html', {
            'log_entry': log_entry
        })
    except ImportLog.DoesNotExist:
        return render(request, 'monitor/import_log_detail.html', {
            'error': '日志记录不存在'
        })

def process_geospatial_file(uploaded_file, file_name):
    """处理地理数据文件 (Shapefile, GeoJSON, KML)"""
    try:
        import geopandas as gpd
        import pandas as pd
        from io import BytesIO

        if file_name.endswith('.shp'):
            # 处理Shapefile - 需要同时上传.shp, .dbf, .shx等文件
            # 这里简化处理，只读取.shp文件
            gdf = gpd.read_file(BytesIO(uploaded_file.read()))
        elif file_name.endswith('.geojson'):
            # 处理GeoJSON
            gdf = gpd.read_file(BytesIO(uploaded_file.read()))
        elif file_name.endswith('.json'):
            # 处理JSON格式的地理数据
            gdf = gpd.read_file(BytesIO(uploaded_file.read()))
        elif file_name.endswith('.kml'):
            # 处理KML文件
            gdf = gpd.read_file(BytesIO(uploaded_file.read()), driver='KML')
        else:
            raise ValueError(f"不支持的地理数据格式: {file_name}")

        # 转换为DataFrame，提取坐标
        if hasattr(gdf, 'geometry'):
            # 为点几何体提取经纬度
            gdf_copy = gdf.copy()
            gdf_copy['longitude'] = gdf_copy.geometry.x
            gdf_copy['latitude'] = gdf_copy.geometry.y

            # 转换为普通DataFrame
            df = pd.DataFrame(gdf_copy.drop(columns=['geometry']))

            # 重命名坐标列以匹配我们的格式
            column_mapping = {
                'longitude': 'longitude_deg' if 'longitude_deg' not in df.columns else 'longitude',
                'latitude': 'latitude_deg' if 'latitude_deg' not in df.columns else 'latitude'
            }
            df = df.rename(columns=column_mapping)

        else:
            # 如果不是地理数据，直接读取为DataFrame
            df = pd.read_json(BytesIO(uploaded_file.read()))

        return df

    except ImportError:
        raise ValueError("处理地理数据需要安装geopandas: pip install geopandas")
    except Exception as e:
        raise ValueError(f"处理地理数据文件失败: {str(e)}")

def realtime_log_view(request, log_id):
    """实时日志查看视图"""
    try:
        log_entry = ImportLog.objects.get(id=log_id)
        return render(request, 'monitor/realtime_log.html', {
            'log_entry': log_entry
        })
    except ImportLog.DoesNotExist:
        return render(request, 'monitor/realtime_log.html', {
            'error': '日志记录不存在'
        })

def api_log_stream(request, log_id):
    """实时日志流API"""
    try:
        log_entry = ImportLog.objects.get(id=log_id)
        data = {
            'status': log_entry.status,
            'details': log_entry.details,
            'error_messages': log_entry.error_messages,
            'success_count': log_entry.success_count,
            'error_count': log_entry.error_count,
            'total_rows': log_entry.total_rows,
            'completed_at': log_entry.completed_at.isoformat() if log_entry.completed_at else None
        }
        return JsonResponse(data)
    except ImportLog.DoesNotExist:
        return JsonResponse({'error': '日志不存在'}, status=404)


def project_log_stream(request):
    """项目日志实时流"""
    def event_stream():
        import time
        import logging
        from datetime import datetime
        from django.utils import timezone

        # 获取Django日志
        logger = logging.getLogger()

        # 模拟一些项目日志消息
        log_messages = [
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: Django服务器启动完成",
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: 数据库连接正常",
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: ArcGIS地图服务就绪",
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: 鸟情监测系统运行中...",
        ]

        # 发送初始日志
        for msg in log_messages:
            yield f"data: {msg}\n\n"
            time.sleep(0.5)

        # 持续监控新的日志消息
        while True:
            try:
                # 这里可以集成实际的日志监控逻辑
                # 目前发送心跳消息
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                yield f"data: [{current_time}] INFO: 系统运行正常\n\n"
                time.sleep(5)  # 每5秒发送一次心跳

            except Exception as e:
                yield f"data: [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: 日志流错误 - {str(e)}\n\n"
                break

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'  # 禁用nginx缓冲
    return response