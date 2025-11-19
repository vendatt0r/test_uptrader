from django.db import models
from django.urls import reverse, NoReverseMatch


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    title = models.CharField(max_length=200)
    # один из двух: либо явно указанный URL, либо имя named-url (без args)
    url = models.CharField(max_length=500, blank=True, help_text="явный URL (например /about/)")
    named_url = models.CharField(
        max_length=200,
        blank=True,
        help_text="named url (reverse name). Аргументы не поддерживаются в этой версии."
    )
    # позиция/порядок — простой способ контролировать порядок
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    def get_url(self):
        """
        Возвращает итоговый URL: сначала пытается named_url через reverse,
        затем поле url, иначе '#' — не делает дополнительных запросов.
        NOTE: Не поддерживаем передачу args/kwargs для именованных урлов в этой реализации.
        """
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                # если named url не найден — fallback на url
                pass
        return self.url or "#"
