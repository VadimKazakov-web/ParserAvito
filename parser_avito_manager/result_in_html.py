import re


class ResultInHtml:

    def __init__(self):
        self.header_content_pattern = re.compile(r'[{]title_content[}]')
        self.total_views_pattern = re.compile(r'[{]total_views_content[}]')
        self.today_views_pattern = re.compile(r'[{]today_views_content[}]')
        self.review_count_pattern = re.compile(r'[{]review_count_content[}]')
        self.path_of_base_html = 'parser_avito_manager/index.html'
        self.str_base_html = self.read_base_html()

    def read_base_html(self):
        with open(self.path_of_base_html, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def preparation_title(counter):
        content = "Oтсканировано: {length} объявлений".format(length=counter)
        return content

    @staticmethod
    def preparation_elem(elem):
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

    def preparation_elements(self, data):
        result = ""
        for elem in data:
            text = self.preparation_elem(elem)
            result += text
        return result

    def write_result(self, file_name, data, count):
        total_views = data.get("total_views")
        today_views = data.get("today_views")
        reviews = data.get("reviews")
        with open(file_name, 'w', encoding='utf-8') as file:
            content = self.header_content_pattern.sub(self.preparation_title(count), self.str_base_html)
            content = self.total_views_pattern.sub(self.preparation_elements(total_views), content)
            content = self.today_views_pattern.sub(self.preparation_elements(today_views), content)
            content = self.review_count_pattern.sub(self.preparation_elements(reviews), content)
            file.write(content)

