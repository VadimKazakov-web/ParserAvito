class ResultInHtml:

    def __init__(self):
        self.part_1 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Result</title>
    <style>
        * {
            box-sizing: border-box;
            padding: 0;
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 97%;
            margin: 0 auto;
        }
        .main_title {
            margin-bottom: 10px;
        }
        .elem {
            display: flex;
            flex-direction: column;
            width: 100%;
            border-radius: 5px;
            margin: 8px;
            background-color: antiquewhite;
            padding: 5px;
            max-width: 1400px;
        }
        .id {
            color: gray;
        }
        .title {
            font-size: 20px;
        }
        .link {
            display: block;
            font-size: 15px;
            word-break: break-all;
        }
        .info {
            display: flex;
            align-items: center;
        }
        .info span {
            margin-right: 10px;
            padding: 5px;
            font-size: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        """
        self.part_2 = """
    </div>
</body>
</html>
        """

    @staticmethod
    def preparation_title(counter):
        title = """
        <h1 class="main_title">
            Oтсканировано: {length} объявлений
        </h1>
        """.format(length=counter)
        return title

    @staticmethod
    def preparation_text(elem):
        text = """
        <div class="elem">
        <span class="id">№ {id}</span>
        <h3 class="title">
            {title}
        </h3>
        <a class="link" href="{link}">
            {link_short}
        </a>
        <div class="info">
            <span class="date">
                {date}
            </span>
            <span class="total_views">
                просмотров всего: {total_views}
            </span>
            <span class="today_views">
                просмотров сегодня: {today_views}
            </span>
        </div>
    </div>
    """.format(id=elem.get("id"), title=elem.get("title"), link=elem.get("link"),
               link_short=elem.get("link")[0:100]+"...",
               date=elem.get("date"), total_views=elem.get("total_views"),
               today_views=elem.get("today_views"))
        return text

    def write_result(self, file_name, data, count):
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(self.part_1)
            title = self.preparation_title(count)
            file.write(title)
            for elem in data:
                text = self.preparation_text(elem)
                file.write(text)
            file.write(self.part_2)
