class ResultInHtml:

    def __init__(self):
        self.part_1 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        * {
            box-sizing: border-box;
            padding: 0;
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
        }
        .container {
            width: 97%;
            margin: 0 auto;
        }
        .main_title {
            margin-bottom: 20px;
        }
        .options {
            margin-bottom: 20px;
        }
        .btn {
            margin-right: 15px;
            margin-bottom: 15px;
            padding: 5px 10px;
            cursor: pointer;
        }
        .result {
            display: none !important;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .elem {
            display: flex;
            flex-direction: column;
            width: 100%;
            border-radius: 5px;
            margin-bottom: 8px;
            background-color: antiquewhite;
            padding: 5px;
        }
        .id {
            color: gray;
        }
        .title {
            font-size: 20px;
        }
        .link {
            display: block;
            width: 100%;
            font-size: 15px;
            word-break: break-all;
        }
        .info {
            padding: 10px 0;
            max-width: 700px;
        }
        .info td {
            padding: 0 3px;
        }
        .display-block {
            display: block !important;
        }
    </style>
</head>
<body>
    <div class="container">
        """
        self.part_2 = """
    </div>
    <script>
        let btn_total_view = document.querySelector('#btn_total_view');
        let btn_today_view = document.querySelector('#btn_today_view');
        let btn_review = document.querySelector('#btn_review');
        let results = document.querySelectorAll('.result');

        btn_total_view.addEventListener("click", () => {
            results.forEach((elem) => {
                elem.classList.remove('display-block');
            })
            block_total_views.classList.add('display-block');
        })

        btn_today_view.addEventListener("click", () => {
            results.forEach((elem) => {
                elem.classList.remove('display-block');
            })
            block_today_views.classList.add('display-block');
        })

        btn_review.addEventListener("click", () => {
            results.forEach((elem) => {
                elem.classList.remove('display-block');
            })
            block_review_count.classList.add('display-block');
        })

        let block_total_views = document.querySelector('#block_total_views');
        let block_today_views = document.querySelector('#block_today_views');
        let block_review_count = document.querySelector('#block_review_count');
    </script>
</body>
</html>
        """

    @staticmethod
    def preparation_title(counter):
        title = """
        <h1 class="main_title">
            Oтсканировано: {length} объявлений
        </h1>
        <div class="options">
            <button id="btn_total_view" class="btn">
                по просмотрам за всё время
            </button>
            <button id="btn_today_view" class="btn">
                по просмотрам за сегодня
            </button>
            <button id="btn_review" class="btn">
                по отзывам
            </button>
        </div>
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

    def write_result(self, file_name, data_list, count):
        data_list = enumerate(data_list)
        block_list = ['<div id="block_total_views" class="result display-block">',
                      '<div id="block_today_views" class="result">',
                      '<div id="block_review_count" class="result">'
                      ]
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(self.part_1)
            title = self.preparation_title(count)
            file.write(title)
            for index, data in data_list:
                file.write(block_list[index])
                for elem in data:
                    text = self.preparation_text(elem)
                    file.write(text)
                file.write("""
                            </div>
                            """)
            file.write(self.part_2)
