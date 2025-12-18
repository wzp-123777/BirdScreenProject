from django.db import models
from django.utils import timezone

class BirdSpecies(models.Model):
    name = models.CharField(max_length=100, verbose_name="鸟类名称")
    danger_level = models.IntegerField(default=1, verbose_name="危险等级(1-10)")
    description = models.TextField(blank=True, verbose_name="描述")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "鸟类信息"
        verbose_name_plural = "鸟类信息"

class BirdRecord(models.Model):
    RISK_LEVEL_CHOICES = [
        ('low', '低风险'),
        ('medium', '中风险'),
        ('high', '高风险'),
    ]

    species = models.ForeignKey(BirdSpecies, on_delete=models.CASCADE, verbose_name="鸟种")
    quantity = models.IntegerField(verbose_name="数量")
    location = models.CharField(max_length=200, verbose_name="发现位置")
    latitude = models.FloatField(null=True, blank=True, verbose_name="纬度")
    longitude = models.FloatField(null=True, blank=True, verbose_name="经度")
    intrusion_reason = models.CharField(max_length=200, blank=True, verbose_name="入侵原因")
    record_time = models.DateTimeField(default=timezone.now, verbose_name="记录时间")
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, default='low', verbose_name="风险等级")
    notes = models.TextField(blank=True, verbose_name="备注")

    def save(self, *args, **kwargs):
        # Simple risk calculation logic (Example)
        # Risk = Species Danger * Quantity
        score = self.species.danger_level * self.quantity
        if score > 50:
            self.risk_level = 'high'
        elif score > 20:
            self.risk_level = 'medium'
        else:
            self.risk_level = 'low'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "鸟情记录"
        verbose_name_plural = "鸟情记录"

class Airport(models.Model):
    """机场信息模型"""
    AIRPORT_TYPES = [
        ('large_airport', '大型机场'),
        ('medium_airport', '中型机场'),
        ('small_airport', '小型机场'),
        ('heliport', '直升机场'),
        ('seaplane_base', '水上飞机基地'),
        ('balloonport', '热气球场'),
        ('closed', '已关闭'),
    ]

    ident = models.CharField(max_length=10, unique=True, verbose_name="机场标识符")
    name = models.CharField(max_length=200, verbose_name="机场名称")
    airport_type = models.CharField(max_length=20, choices=AIRPORT_TYPES, default='small_airport', verbose_name="机场类型")

    latitude = models.FloatField(verbose_name="纬度")
    longitude = models.FloatField(verbose_name="经度")
    elevation_ft = models.IntegerField(null=True, blank=True, verbose_name="海拔高度(英尺)")

    continent = models.CharField(max_length=2, blank=True, verbose_name="大洲")
    iso_country = models.CharField(max_length=2, verbose_name="国家代码")
    iso_region = models.CharField(max_length=7, verbose_name="地区代码")
    municipality = models.CharField(max_length=100, blank=True, verbose_name="城市")

    scheduled_service = models.CharField(max_length=3, default='no', verbose_name="定期航班")
    icao_code = models.CharField(max_length=4, blank=True, verbose_name="ICAO代码")
    iata_code = models.CharField(max_length=3, blank=True, verbose_name="IATA代码")
    gps_code = models.CharField(max_length=10, blank=True, verbose_name="GPS代码")
    local_code = models.CharField(max_length=10, blank=True, verbose_name="本地代码")

    home_link = models.URLField(blank=True, verbose_name="官网链接")
    wikipedia_link = models.URLField(blank=True, verbose_name="维基百科链接")
    keywords = models.TextField(blank=True, verbose_name="关键词")

    def __str__(self):
        return f"{self.name} ({self.ident})"

    class Meta:
        verbose_name = "机场信息"
        verbose_name_plural = "机场信息"

class ImportLog(models.Model):
    """导入日志模型"""
    LOG_TYPES = [
        ('bird', '鸟情数据'),
        ('airport', '机场数据'),
    ]

    log_type = models.CharField(max_length=10, choices=LOG_TYPES, verbose_name="日志类型")
    file_name = models.CharField(max_length=255, verbose_name="文件名")
    file_size = models.IntegerField(verbose_name="文件大小(bytes)")
    total_rows = models.IntegerField(default=0, verbose_name="总行数")
    success_count = models.IntegerField(default=0, verbose_name="成功导入数")
    error_count = models.IntegerField(default=0, verbose_name="错误数")
    status = models.CharField(max_length=20, default='processing', verbose_name="状态")
    details = models.TextField(blank=True, verbose_name="详细信息")
    error_messages = models.TextField(blank=True, verbose_name="错误信息")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="完成时间")

    def __str__(self):
        return f"{self.get_log_type_display()} - {self.file_name} ({self.created_at.strftime('%H:%M:%S')})"

    class Meta:
        verbose_name = "导入日志"
        verbose_name_plural = "导入日志"
        ordering = ['-created_at']