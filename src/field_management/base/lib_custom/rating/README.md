1. Module tham khảo: Tour
1. Settings:
    Tự động approve các rating của customer ```RATING_APPROVE_AUTO = True```
1. Các tên model phải cố định như trong ví dụ, không được đổi tên, gồm 4 model

    ```
    class ObjectRate(RateBaseModel)
    class ObjectRateReply(RateReplyBaseModel)
    class ObjectRateGallery(RateGalleryBase)
    class ObjectRateLike(RateLikeBase)
    ```

1. Trong model ObjectRate, khai báo thêm 1 column, khóa ngoại tới object chính cần được rate, tên cột là cố định
obj_main

    ```
    obj_main = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Tour")
    ```

1. Trong object main này (Tour), phải có 2 cột thống kê lại số rate_avg và rate_count

    ```
    rate_avg = models.FloatField(default=0, verbose_name='Giá trị rate trung bình')
    rate_count = models.FloatField(default=0, verbose_name='Tổng số rate')
    ```

1. Khai báo thêm url và view
