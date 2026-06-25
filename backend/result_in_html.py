import re
from backend.index import base


class ResultInHtmlMixin:
    """
    Запись результатов в html файл
    """
    _header_content_pattern = re.compile(r'[{]title_content[}]')
    _total_views_pattern = re.compile(r'[{]total_views_content[}]')
    _today_views_pattern = re.compile(r'[{]today_views_content[}]')
    _review_count_pattern = re.compile(r'[{]review_count_content[}]')
    _str_base_html = base

    @classmethod
    def create_result_file(cls, file_name, count):
        cls._file_name = file_name
        cls._count = count
        with open(cls._file_name, 'w', encoding='utf-8') as file:
            content = cls._header_content_pattern.sub(cls._preparation_title(cls._count), cls._str_base_html)
            file.write(content)
            file.flush()

    @staticmethod
    def _preparation_title(counter):
        content = "Сканировано: {length} объявлений".format(length=counter)
        return content

    @staticmethod
    def _preparation_elem(elem):
        text = """
        <div class="elem">
        <span class="id">№ {id}</span>
        <h3 class="title">
            {title}
        </h3>
        <a class="link" href="{link}">
            {link_short}
        </a>
        <table class="info">
            <tr>
            <td class="date">
                {date}
            </td>
            <td class="total_views">
                просмотров всего: {total_views}
            </td>
            <td class="today_views">
                просмотров сегодня: {today_views}
            </td>
            </tr>
            <tr>
            <td class="rating">
                рейтинг: {rating}
            </td>
            <td class="reviews">
                кол-во отзывов: {reviews}
            </td>
            </tr>
        </table>
    </div>
    """.format(id=elem.get("id"), title=elem.get("title"), link=elem.get("link"),
               link_short=elem.get("link", lambda _: "link" * 30)[0:100]+"...",
               date=elem.get("date"), total_views=elem.get("total_views"),
               today_views=elem.get("today_views"), rating=elem.get("rating"), reviews=elem.get("reviews"))
        return text

    def _preparation_elements(self, data):
        result = ""
        for elem in data:
            text = self._preparation_elem(elem)
            result += text
        return result

    def _write(self, pattern, data):
        with open(self._file_name, 'r+', encoding='utf-8') as file:
            content = pattern.sub(self._preparation_elements(data), file.read())
            file.seek(0)
            file.write(content)
            file.truncate()
            file.flush()

    def write_result(self, flag, data):
        if flag == "total_views":
            self._write(pattern=self._total_views_pattern, data=data)
        elif flag == "today_views":
            self._write(pattern=self._today_views_pattern, data=data)
        elif flag == "reviews":
            self._write(pattern=self._review_count_pattern, data=data)
