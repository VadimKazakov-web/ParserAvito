
Учебно-тренировочный проект парсера сайта www.avito.ru,
целью данного проекта было изучение и применение на практике: <br>

* [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/) - для серверной части <br>
* [tkinter](https://docs.python.org/3/library/tkinter.html) - для графического интерфейса. <br>

Данная программа скомпилирована из исходного кода в один exe-файл <br>
с помощью [pyinstaller](https://pypi.org/project/pyinstaller/) и находится в хранилище S3.
<figure>
    <img src="https://s3.twcstorage.ru/parser-avito-download/githab_image/parser_avito.png" width="500" alt="интерфейс программы">
    <figcaption>пользовательский интерфейс программы</figcaption>
</figure>

<h2>Коротко о дизайне</h2>

<h3>Интерфейс</h3>
Окно программы выполнено с использованием стандартной библиотеки tkinter.
Код организован в виде иерархии пакетов, для повышения читаемости, где каждый пакет является фреймом или другим логическим блоком программы.
<figure>
    <img src="https://s3.twcstorage.ru/parser-avito-download/githab_image/hierarchy_interface.png" width="500" alt="иерархия пакетов">
    <figcaption>иерархия пакетов</figcaption>
</figure>



