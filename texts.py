# -*- coding: utf-8 -*-

helpText = '/help - выводит этот текст\n/book - переходит к рекомендации книг'
startText = 'Этот бот предназначен для получения жанровых рекомендаций книг из базы Фантлаба (https://fantlab.ru/). Для начала работы наберите команду /book или нажмите на кнопку внизу'
botErrorText = 'Произошла ошибка. Пожалуйста, начните работу с ботом заново и сообщите разработчику (@qiray) о случившемся.'
pleaseWaitText = "Пожалуйста, подождите, выбираем книгу специально для вас..."
showRecomendsText = "Перейти к рекомендациям"
iwantmoreText = "Хочу еще такого же"
startagainText= "Не, давай по новой"
pleaseWaitTheSameText = "Хорошо, подбираем еще парочку похожих книг"

requestStepsArray = [
	[
		["Фэнтези", "wg19=on", 0], 
		["Фантастика", "wg1=on", 0],
		['Не важно', "NONE", 0]
	],
	[
		["На Земле", "&wg69=on&wg89=on", 1], 
		["Где-то в другом мире", "&wg78=on&wg88=on&wg91=on&wg92=on&wg129=on&wg213=on", 1],
		['Не важно', "NONE", 1]
	], 
	[
		["Далеко в прошлом", "&wg93=on&wg94=on&wg95=on&wg96=on&wg97=on&wg98=on&wg99=on", 2], 
		["В наши дни", "&wg100=on&wg101=on", 2],
		["В будущем", "&wg102=on&wg103=on&wg104=on", 2],
		['Не важно', "NONE", 2]
	],
	[
		["Наши", "&lang=rus", 3], 
		["Зарубежные", "&lang=for", 3],
		['Не важно', "NONE", 3]
	],
	[
		["Роман", "&form=nov", 4], 
		["Повесть или рассказ", "&form=sto", 4],
		['Не важно', "NONE", 4]
	]
]
	
requestNamesArray = ["Что читаем?", "Где разворачивается действие?", "Когда происходят события?", "И кто же авторы?", "А размер имеет значение?"]

fixRequestString = "wg1=on&wg19=on&wg33=on&wg30=on&wg31=on&wg32=on&wg34=on&wg35=on&wg225=on&wg36=on&wg37=on&wg38=on&wg39=on&wg160=on&wg116=on&lang=&form="

top100questions = [
	[
		'С чего хотите начать?', 
		0,
		[
			['Фантастика', 2],
			['Фэнтези', 3],
			['И того, и другого', 50],
			['Я предпочитаю книжки с картинками', 51],
			['Как насчёт ужасов?', 52],
			['Откланиваюсь. Пойду-ка лучше в раздел с Донцовой.', 53]
		]
	],
	[
		'Вам нравится киберпанк?',
		1,
		[
			['Да. Панки, хой!', 4],
			['Не, спасибо, я с ними пару раз в автобусе ехал.', 5],
			['Можно. Тогда лучше что-то весёлое про киберпространство', '9769', 'Криптономикон', 'Нил Стивенсон']
		]
	],
	[
		'Вас расстроит, если в книге не будет *шрамированного подростка в магической школе*?',
		1,
		[
			['Да. Без Поттера и книга не книга, и фильм не фильм!', '188170', 'Имя ветра', 'Патрик Ротфусс'],
			['Нет. К Вольдемору Поттера!', 6]
		]
	],
	[
		'Суровый нуар, викторианская Англия или катаны и самураи?',
		2,
		[
			['Суровый нуар. Да, я не хочу быть пай-мальчиком.', '2654', 'Нейромант', 'Уильям Гибсон'],
			['Викторианская Англия. Ах, этот незабываемый хруст викторианских булок!', '9767', 'Алмазная эпоха', 'Нил Стивенсон'],
			['Самураи. Только настоящий Путь Самурая.', '9765', 'Лавина', 'Нил Стивенсон']
		]
	],
	[
		'Как насчёт громких взрывов в вакууме?',
		2,
		[
			['О да! Будет скафандр, будут путешествия (через тернии к звёздам)', 7],
			['Нет. Я предпочитаю держать ноги не вакууме, а на какой-нибудь твёрдой опоре, вроде Земли', 8],
			['Ну может быть. Хотя меня терзают смутные сомнения. А можно не покидать Солнечную систему?', 9]
		]
	],
	[
		'А вы с фэнтези хорошо знакомы?',
		3,
		[
			['Неа. Мои бедные стальные нервы её переносят с трудом.', 69],
			['Да. О, Элберет и Земноморье!', 10],
			['Немного. Я чего-то такое про Тотошку и дорогу из жёлтого кирпича в детстве читал.', '81650', 'Ведьма. Жизнь и времена Западной колдуньи из страны Оз', 'Грегори Магуайр']
		]
	],
	[
		'Как насчёт военной фантастики?',
		5,
		[
			['О да! Я этих зергов накрошил немеренно!', 11],
			['Спасибо, не надо. А нет ли у вас что-нибудь про первый контакт?', 12],
			['Можно. Хотя мне бы до войны космос поисследовать.', 13]
		]
	],
	[
		'А как насчёт приключений внутри Земли?',
		5,
		[
			['Да. Звучит интересно. Дайте два!', 14],
			['Нет. Эй, умник, я сказал на поверхности, а не под ней.', 15]
		]
	],
	[
		'ОК. А от Земли отлетать будем?',
		5,
		[
			['Ну нет. У меня боязнь открытого пространства. Ну вот разве что Марс?', 16],
			['Конечно же', '9957', '2001: Космическая одиссея', 'Артур Кларк']
		]
	],
	[
		'Как Артуриана?',
		6,
		[
			['Да я даже "Янки при дворе короля Артура" только из-за Артура и прочёл.', 17],
			['Нет', 18]
		]
	],
	[
		'И кого укрощать будем?',
		7,
		[
			['Жуков', '2796', 'Звёздный десант', 'Роберт Хайнлайн'],
			['Жуков. Но из глубин Космоса.', '4670', 'Игра Эндера', 'Орсон Скотт Кард'],
			['Гуманоидов. Чтобы две руки, две ноги были', '15912', 'Бесконечная война', 'Джо Холдеман'],
			['Империю', '4325', 'Дюна', 'Фрэнк Герберт'],
			['Землян. Вернее, колиниальную администрацию, угнетающую свободолюбивых лунян.', '2802', 'Луна жёстко стелет', 'Роберт Хайнлайн'],
			['Всех. Кого встретим, с тем и воюем.', '29460', 'Война старика', 'Джон Скальци']
		]
	],
	[
		'И с какими пришельцами Вам бы хотелось повстречаться?',
		7,
		[
			['Воинственными.', '9457', 'Война миров', 'Герберт Уэллс'],
			['Равнодушными. Которым безразлична Земля и её обитатели.', '9961', 'Свидание с Рамой', 'Артур Кларк'],
			['Мирными', '10140', 'Конец детства', 'Артур Кларк'],
			['Мудрыми. Которые хотят позаботиться о человечестве.', '106908', 'Контакт', 'Карл Саган'],
			['Быстроразмножающимися.', '23283', 'Мошка в зенице Господней', 'Ларри Нивен и Джерри Пурнелл']
		]
	],	
	[
		'Далёкая-предалёкая Галактика?',
		7,
		[
			['Да. И лучше бы ещё и давным давно.', '14938', 'Наследник Империи', 'Тимоти Зан'],
			['Нет. Знаю, что хотите предложить.', 19]
		]
	],	
	[
		'Под сушей или под морем?',
		8,
		[
			['Под землёй, конечно же.', '7189', 'Путешествие к центру Земли', 'Жюль Верн'],
			['Под водой. Ах, море-море', '7182', 'Двадцать тысяч лье под водой', 'Жюль Верн']
		]
	],	
	[
		'Ну раз я - умник, скажите, что больше интересно: политика, религия или философия?',
		8,
		[
			['Анархия - мать порядка.', 20],
			['Религия - опиум для народа.', 21],
			['Я мыслю - следовательно, существую.', '5353', 'Мечтают ли андроиды об электроовцах?', 'Филипп К. Дик'],
			['Ну уж нет. В прошлый раз с приятелями про Сталина заговорили, так у меня теперь зуба нет. А чего-нибудь про путешествия во времени есть или ещё чего интересненькое?', 22]
		]
	],	
	[
		'Хм, Марс. А как бы Вам хотелось увидеть Красную планету?',
		9,
		[
			['Через окошко, причём земляничное.', '5149', 'Марсианские хроники', 'Рей Брэдбери'],
			['Глазами специалиста по терроформированию.', '18286', 'Красный Марс', 'Ким Стенли Робинсон'],
			['Сквозь волшебное зеркало.', '11139', 'Космическая трилогия', 'Клайв Льюис'],
		]
	],	
	[
		'А кто из героев самый-самый?',
		10,
		[
			['Моргана', '16699', 'Туманы Авалона', 'Мэрион Брэдли'],
			['Мерлин', '10805', 'Хрустальный грот', 'Мэри Стюарт'],
			['Артур', '22020', 'Король Былого и Грядущего', 'Теренс Х. Уайт']
		]
	],	
	[
		'А действие в нашем мире?',
		10,
		[
			['Да. Ну да, я - городской ребёнок.', 23],
			['Нет. Тут скучно и уныло, мне бы другой глобус.', 24],
			['Можно и так. Каждое лето в детстве я проводил в маленьком городке, где жила бабушка.', '5219', 'Что-то страшное грядёт', 'Рэй Брэдбери'],
		]
	],	
	[
		'Любите хорошую шутку?',
		13,
		[
			['А то. Я - испытанный остряк.', '2076', 'Путеводитель по галактике для путешествующих автостопом', 'Дуглас Адамс'],
			['Не в книгах. Да и вообще, у меня некоторые проблемы с чувством юмора.', 25],
			['Можно. Только чтобы: взрывы, стрельба, пара весёлых моментов, и снова стрельба.', '13789', 'Культура', 'Иен Бэнкс']
		]
	],	
	[
		'Что вам интереснее?',
		15,
		[
			['Феминизм', '2051', 'Левая рука Тьмы', 'Урсула Ле гуин'],
			['Коммунизм', 'Обделённые', 'Урсула Ле Гуин']
		]
	],
	[
		'Чем будем дурманить голову?',
		15,
		[
			['Христианством', '13076', 'Страсти по Лейбовицу', 'Уолтер Миллер младший'],
			['Гуманизмом', '2797', 'Чужак в чужой стране', 'Роберт Хайнлайн']
		]
	],
	[
		'Олично. А лучше что-нибудь классическое или наоборот посовременнее?',
		15,
		[
			['Современное', '33826', 'Doomsday Book', 'Конни Уиллис'],
			['Классику', '9452', 'Машина времени', 'Герберт Уэллс'],
			['Ой, не надо лучше. Чего-то я заговорился уже. Лучше мистику какую-нибудь или триллер посоветуйте.', 26]
		]
	],	
	[
		'А под городом можно повстречаться с богами?',
		18,
		[
			['Да. С одной стороны, чтобы что-то мифологическое, но с другой, чтобы про современность', '10134', 'Американские боги', 'Нил Гейман'],
			['Нет. Чтобы и без богов там целый мир был.', '10133', 'Задверье', 'Нил Гейман']
		]
	],
	[
		'А вестерны нравятся?',
		18,
		[
			['А то! У меня и шляпа есть как у Клинт Иствуда.', '424', 'Тёмная башня', 'Стивен Кинг'],
			['Нет. Старьё. Да и в карты постоянно режутся, а я не очень в этом деле разбираюсь.', 27]
		]
	],	
	[
		'Ага, чувствуется закваска настоящего учёного, не так ли?',
		19,
		[
			['Да. А если уж и приходится лирику читать, то предпочитаю твёрдую научную фантастику.', 28],
			['Не угадали. Просто предпочитаю, когда экшена побольше.', 29]
		]
	],	
	#[
		#'Уверены? Так мистика или триллер?'],
			#['Мистика'],
			#['Триллер',
		#<button id="q26-Back" class="btnBack" onClick="goBack('q26', 'q22')">< Назад</button>
		#<script>
			#$('#q26-mystery').click(function() {$('#q26').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q26', '779', 'Стальные пещеры', 'Айзек Азимов', '')); $('#leafNode').show('fast');});});
			#$('#q26-thriller').click(function() {$('#q26').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q26', '23432', 'Молот Люцифера', 'Ларри Нивен и Джереми Пурнелл', '')); $('#leafNode').show('fast');});});
		#</script>
	#],	
	#[
		#'Животные больше интересны?'],
			#['Да'],
			#['Нет',
#Я когда рекламу фонда диких животных вижу, у меня слёзы на глазах наворачиваются.
#У меня на них аллергия.
		#<button id="q27-Back" class="btnBack" onClick="goBack('q27', 'q24')">< Назад</button>
		#<script>
			#$('#q27-Yes').click(function() {$('#q27').hide('fast', function() {$('#q30').show('fast');});});
			#$('#q27-No').click(function() {$('#q27').hide('fast', function() {$('#q31').show('fast');});});
		#</script>
	#],	
	#[
		#'Что изучаете?'],
			#['Историю'],
			#['Я - инженер'],
			#['IT-технологии',
		#<button id="q28-Back" class="btnBack" onClick="goBack('q28', 'q25')">< Назад</button>
		#<script>
			#$('#q28-morgan').click(function() {$('#q28').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q28', '95', 'Основание', 'Айзек Азимов', '')); $('#leafNode').show('fast');});});
			#$('#q28-merlin').click(function() {$('#q28').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q28', '23276', 'Мир-кольцо', 'Ларри Нивен', '')); $('#leafNode').show('fast');});});
			#$('#q28-arthur').click(function() {$('#q28').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q28', '7019', 'Пламя над бездной', 'Вернон Виндж', '')); $('#leafNode').show('fast');});});
		#</script>
	#],	
	#[
		#'А к сериалам как относитесь?'],
			#['Нормально'],
			#['Плохо',

#Не за какие коврижки.
		#<button id="q29-Back" class="btnBack" onClick="goBack('q29', 'q25')">< Назад</button>
		#<script>
			#$('#q29-Yes').click(function() {$('#q29').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q29', '5385', 'Барраярский цикл', 'Лоис Макмастер Буджолд', '')); $('#leafNode').show('fast');});});
			#$('#q29-No').click(function() {$('#q29').hide('fast', function() {$('#q32').show('fast');});});
		#</script>
	#],	
	#[
		#'Кого бы с удовольствием дома завели?'],
			#['Единорога'],
			#['Кролика'],
			#['Дракона',
		#<button id="q30-Back" class="btnBack" onClick="goBack('q30', 'q27')">< Назад</button>
		#<script>
			#$('#q30-unicorn').click(function() {$('#q30').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q30', '11022', 'Последний единорог', 'Питер Бигль', '')); $('#leafNode').show('fast');});});
			#$('#q30-bunny').click(function() {$('#q30').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q30', '37490', 'Обитатели холмов', 'Ричард Адамс', '')); $('#leafNode').show('fast');});});
			#$('#q30-dragon').click(function() {$('#q30').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q30', '9869', 'Полёт дракона', 'Энн Маккефри', '')); $('#leafNode').show('fast');});});
		#</script>
	#],	
	#[
		#'А к альтернативной истории как относитесь?'],
			#['Люблю'],
			#['Без восторга',
#Ой, жа я пикейный жилет в глубине души, бывает как сяду рассуждать: а что если бы...
#Я и в школе уроки истории просто прогуливал.
		#<button id="q31-Back" class="btnBack" onClick="goBack('q31', 'q27')">< Назад</button>
		#<script>
			#$('#q31-Yes').click(function() {$('#q31').hide('fast', function() {$('#q33').show('fast');});});
			#$('#q31-No').click(function() {$('#q31').hide('fast', function() {$('#q34').show('fast');});});
		#</script>
	#],	
	#[
		#'А ну тогда рассказы, и это замечательно! Роботы или марсиане?'],
			#['Роботы'],
			#['Марсиане',
		#<button id="q32-Back" class="btnBack" onClick="goBack('q32', 'q29')">< Назад</button>
		#<script>
			#$('#q32-robots').click(function() {$('#q32').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q32', '7078', 'Я, робот', 'Айзек Азимов', '')); $('#leafNode').show('fast');});});
			#$('#q32-martians').click(function() {$('#q32').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q32', '5042', 'Человек в картинках', 'Рэй Брэдбери', '')); $('#leafNode').show('fast');});});
		#</script>
	#],	
	#[
		#'Любовь и магия или вражда между волшебниками?'],
			#['Любовь и магия'],
			#['Вражда',
		#<button id="q33-Back" class="btnBack" onClick="goBack('q33', 'q31')">< Назад</button>
		#<script>
			#$('#q33-romance').click(function() {$('#q33').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q33', '189062', 'Kushiel\'s Legacy Series', 'Жаклин Кэри', '')); $('#leafNode').show('fast');});});
			#$('#q33-magicians').click(function() {$('#q33').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q33', '21260', 'Джонатан Стрендж и мистер Норрелл', 'Сюзанна Кларк', '')); $('#leafNode').show('fast');});});
		#</script>
	#],	
	#[
		#'Готовы зарыться в цикл?'],
			#['Да'],
			#['Нет'],
			#['Можно попробовать',
#Я дважды уже выбирал, сколько можно?
#Не хочу, чтобы чтение становилось одноообразным.
#А вот чтобы отдельные книги каких-то циклов можно? 
		#<button id="q34-Back" class="btnBack" onClick="goBack('q34', 'q31')">< Назад</button>
		#<script>
			#$('#q34-Yes').click(function() {$('#q34').hide('fast', function() {$('#q35').show('fast');});});
			#$('#q34-No').click(function() {$('#q34').hide('fast', function() {$('#q36').show('fast');});});
			#$('#q34-Maybe').click(function() {$('#q34').hide('fast', function() {$('#q37').show('fast');});});
		#</script>
	#],	
	#[
		#'А цикл должен иметь окончание?'],
			#['Да'],
			#['Не обязательно',

#Мне нравится чувство ожидания, так что пусть оно длится годами.
		#<button id="q35-Back" class="btnBack" onClick="goBack('q35', 'q34')">< Назад</button>
		#<script>
			#$('#q35-Yes').click(function() {$('#q35').hide('fast', function() {$('#q38').show('fast');});});
			#$('#q35-No').click(function() {$('#q35').hide('fast', function() {$('#q39').show('fast');});});
		#</script>
	#],	
	#[
		#'Пираты должны быть?'],
			#['Да'],
			#['Нет',
#Конечно с пиратами!
#К морским чертям пиратов.
		#<button id="q36-Back" class="btnBack" onClick="goBack('q36', 'q34')">< Назад</button>
		#<script>
			#$('#q36-pirates').click(function() {$('#q36').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q36', '286966', 'Принцесса-невеста', 'Уильям Голдман', '')); $('#leafNode').show('fast');});});
			#$('#q36-nopirates').click(function() {$('#q36').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q36', '10825', 'Звёздная пыль', 'Нил Гейман', '')); $('#leafNode').show('fast');});});
		#</script>
	#],	
	#[
		#'А что вам больше нравится'],
			#['Сатира'],
			#['Сатира'],
			#['Комедия',
#на бюрократические организации
#на церковь
#положений
		#<button id="q37-Back" class="btnBack" onClick="goBack('q37', 'q34')">< Назад</button>
		#<script>
			#$('#q37-unicorn').click(function() {$('#q37').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q37', '1951', 'Опочтарение', 'Терри Пратчетт', '')); $('#leafNode').show('fast');});});
			#$('#q37-bunny').click(function() {$('#q37').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q37', '1722', 'Мелкие боги', 'Терри Пратчетт', '')); $('#leafNode').show('fast');});});
			#$('#q37-dragon').click(function() {$('#q37').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q37', '35756', 'Заклинание для Хамелеона', 'Пирс Энтони', '')); $('#leafNode').show('fast');});});
		#</script>
	#],	
	#[
		#'Словосочетание "фантастика меча и магии" вам заставляют вспомнить что-то хорошее?'],
			#['О, да!'],
			#['Нет',
#Варвары и маги? Да, как это может не нравится?

		#<button id="q38-Back" class="btnBack" onClick="goBack('q38', 'q35')">< Назад</button>
		#<script>
			#$('#q38-Yes').click(function() {$('#q38').hide('fast', function() {$('#q40').show('fast');});});
			#$('#q38-No').click(function() {$('#q38').hide('fast', function() {$('#q41').show('fast');});});
		#</script>
	#],	
	#[
		#'Красивые вершки или вкусные корешки?'],
			#['Высокое <br>фэнтези'],
			#['Релистическое фэнтези',
		#<button id="q39-Back" class="btnBack" onClick="goBack('q39', 'q35')">< Назад</button>
		#<script>
			#$('#q39-high').click(function() {$('#q39').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q39', '224233', 'The Way of Kings', 'Брендон Сандерсонn', '')); $('#leafNode').show('fast');});});
			#$('#q39-low').click(function() {$('#q39').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q39', '4133', 'Песня Льда и Огня', 'Джордж Р. Р. Мартин', '')); $('#leafNode').show('fast');});});
		#</script>
	#],	
	#[
		#'Любите ролевые игры?'],
			#['Да'],
			#['Нет',
		#<button id="q40-Back" class="btnBack" onClick="goBack('q40', 'q38')">< Назад</button>
		#<script>
			#$('#q40-Yes').click(function() {$('#q40').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q40', '3972', 'Дзирт До\'Урден', 'Роберт Сальваторе', '')); $('#leafNode').show('fast');});});
			#$('#q40-No').click(function() {$('#q40').hide('fast', function() {$('#q42').show('fast');});});
		#</script>
	#],
	#[
		#'Какую-нибудь трилогию в старом добром духе?'],
			#['Да'],
			#['Нет'],
			#['Можно',
#Три - моё любимое число.
#В таких случаях я обычно говорю "Семи смертям не бывать, а одной не миновать".
#А чтобы трилогия трилогий можно?
		#<button id="q41-Back" class="btnBack" onClick="goBack('q41', 'q38')">< Назад</button>
		#<script>
			#$('#q41-Yes').click(function() {$('#q41').hide('fast', function() {$('#q43').show('fast');});});
			#$('#q41-No').click(function() {$('#q41').hide('fast', function() {$('#q44').show('fast');});});
			#$('#q41-Maybe').click(function() {$('#q41').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q41', '53650', 'Хроники Томаса Ковенанта, Неверующего', 'Стивен Р. Дональдсон', '')); $('#leafNode').show('fast');});});
		#</script>
	#],	
	#[
		#'Вавары или маги?'],
			#['Маги'],
			#['Варвары',
		#<button id="q42-Back" class="btnBack" onClick="goBack('q42', 'q40')">< Назад</button>
		#<script>
			#$('#q42-wizards').click(function() {$('#q42').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q42', '3378', 'Элрик из Мелнибонэ', 'Майкл Муркок', '')); $('#leafNode').show('fast');});});
			#$('#q42-barbarians').click(function() {$('#q42').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q42', '1382', 'Конан-варвар', 'Роберт Говард', '')); $('#leafNode').show('fast');});});
		#</script>
	#],	
	#[
		#'Значит будете читать о'],
			#['ворах'],
			#['волшебных артефактах'],
			#['убийцах'],
			#['магах',
		#<button id="q43-Back" class="btnBack" onClick="goBack('q43', 'q41')">< Назад</button>
		#<script>
			#$('#q43-thieves').click(function() {$('#q43').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q43', '46393', 'Рожденный туманом', 'Брендон Сандерсон', '')); $('#leafNode').show('fast');});});
			#$('#q43-macguffins').click(function() {$('#q43').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q43', '4960', 'Меч Шаннары', 'Терри Брукс', '')); $('#leafNode').show('fast');});});
			#$('#q43-assassins').click(function() {$('#q43').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q43', '3607', 'Сага о Видящих', 'Робин Хобб', '')); $('#leafNode').show('fast');});});
			#$('#q43-magicians').click(function() {$('#q43').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q43', '3580', 'Имперские войны', 'Раймонд Фэйст', '')); $('#leafNode').show('fast');});});
		#</script>
	#],	
	#[
		#'Ну а пяти-шести книг-то для Вас достаточно?'],
			#['Да'],
			#['Нет',
#Мне надолго хватит.
#Мне нужно как минимум 10.
		#<button id="q44-Back" class="btnBack" onClick="goBack('q44', 'q41')">< Назад</button>
		#<script>
			#$('#q44-Yes').click(function() {$('#q44').hide('fast', function() {$('#q45').show('fast');});});
			#$('#q44-No').click(function() {$('#q44').hide('fast', function() {$('#q46').show('fast');});});
		#</script>
	#],	
	#[
		#'Вам нравятся истории о сиротах, выросших у крестьян?'],
			#['Да/Нет',
#Как не печально, но здесь не из чего выбирать.
		#<button id="q45-Back" class="btnBack" onClick="goBack('q45', 'q44')">< Назад</button>
		#<script>
			#$('#q45-No').click(function() {$('#q45').hide('fast', function() {$('#q47').show('fast');});});
		#</script>
	#],	
	#[
		#'Как насчёт квеста по спасению мира от зла?'],
			#['Да'],
			#['Нет',
#Эпическое противостоя Добра и Зла, пожалуйста.
#Хотелось бы чего-то посложнее.
		#<button id="q46-Back" class="btnBack" onClick="goBack('q46', 'q44')">< Назад</button>
		#<script>
			#$('#q46-Yes').click(function() {$('#q46').hide('fast', function() {$('#q48').show('fast');});});
			#$('#q46-No').click(function() {$('#q46').hide('fast', function() {$('#q49').show('fast');});});
		#</script>
	#],	
	#[
		#'Современное или классическое?'],
			#['Современное'],
			#['Классику',
		#<button id="q47-Back" class="btnBack" onClick="goBack('q47', 'q45')">< Назад</button>
		#<script>
			#$('#q47-modern').click(function() {$('#q47').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q47', '40684', 'Кодекс Алеры', 'Джим Батчер', '')); $('#leafNode').show('fast');});});
			#$('#q47-classic').click(function() {$('#q47').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q47', '4741', 'Белгариад', 'Дэвид Эддингс', '')); $('#leafNode').show('fast');});});
		#</script>
	#],	
	#[
		#'И кто же спасёт мир?'],
			#['Искатель Истины'],
			#['Возрождённый Дракон',
		#<button id="q48-Back" class="btnBack" onClick="goBack('q48', 'q46')">< Назад</button>
		#<script>
			#$('#q48-seeker').click(function() {$('#q48').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q48', '3616', 'Меч Истины', 'Терри Гудкайнд', '')); $('#leafNode').show('fast');});});
			#$('#q48-power').click(function() {$('#q48').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q48', '2699', 'Колесо Времени', 'Роберт Джордан', '')); $('#leafNode').show('fast');});});
		#</script>
	#],
	#[
		#'Сделайте взвешанный выбор, это последнее, что мы Вас спрашиваем.'],
			#['Земля'],
			#['Волнообразное повествование',
#- одна из Теней, которые отбрасывает Амбер.
#Хотелось бы чего-то посложнее.
		#<button id="q49-Back" class="btnBack" onClick="goBack('q49', 'q46')">< Назад</button>
		#<script>
			#$('#q49-seeker').click(function() {$('#q49').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q49', '72', 'Хроники Амбера', 'Роджер Желязны', '')); $('#leafNode').show('fast');});});
			#$('#q49-power').click(function() {$('#q49').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q49', '31518', 'Малазанская <Книга Павших>', 'Стивен Эриксон', '')); $('#leafNode').show('fast');});});
		#</script>
	#],
	#[
		#'Ура, Вы сделали это. Куда отправимся: в будущее или в прошлое?'],
			#['В будущее'],
			#['В прошлое',
		#<button id="q50-Back" class="btnBack" onClick="goBack('q50', 'q1')">< Назад</button>
		#<script>
			#$('#q50-future').click(function() {$('#q50').hide('fast', function() {$('#q54').show('fast');});});
			#$('#q50-past').click(function() {$('#q50').hide('fast', function() {$('#q55').show('fast');});});
		#</script>
	#],
	#[
		#'Супергерои или божество, пережившее пытки?'],
			#['Супергерои'],
			#['Бог сновидений',
		#<button id="q51-Back" class="btnBack" onClick="goBack('q51', 'q1')">< Назад</button>
		#<script>
			#$('#q51-heroes').click(function() {$('#q51').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q51', '216554', 'Хранители', 'Алан Мур', '')); $('#leafNode').show('fast');});});
			#$('#q48-dreammaster').click(function() {$('#q51').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q51', '163035', 'The Sandman. Песочный человек', 'Нил Гейман', '')); $('#leafNode').show('fast');});});
		#</script>
	#],
	#[
		#'Почти не из чего выбирать. Как Вы к вампирам относитесь?'],
			#['Нормально'],
			#['Не очень',

#Мне зомби больше по душе.
		#<button id="q52-Back" class="btnBack" onClick="goBack('q52', 'q1')">< Назад</button>
		#<script>
			#$('#q52-Yes').click(function() {$('#q52').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q52', '121279', 'Солнечный свет', 'Робин Мак-Кинли', '')); $('#leafNode').show('fast');});});
			#$('#q52-No').click(function() {$('#q52').hide('fast', function() {$('#q56').show('fast');});});
		#</script>
	#],
	#[
		#'Мы никому не расскажем. Нравятся трагические истории?'],
			#['Да'],
			#['Нет',
#Я люблю поплакать над книгой.
#Я прошлой ночью в очередной раз посмотрел "Титаник". Так что обойдусь
		#<button id="q53-Back" class="btnBack" onClick="goBack('q53', 'q1')">< Назад</button>
		#<script>
			#$('#q53-Yes').click(function() {$('#q53').hide('fast', function() {$('#q57').show('fast');});});
			#$('#q53-No').click(function() {$('#q53').hide('fast', function() {$('#q58').show('fast');});});
		#</script>
	#],
	#[
		#'Вы часом не слегка тронувшийся математик?'],
			#['Да'],
			#['Нет',
		#<button id="q54-Back" class="btnBack" onClick="goBack('q54', 'q50')">< Назад</button>
		#<script>
			#$('#q54-Yes').click(function() {$('#q54').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q54', '74823', 'Анафем', 'Нил Стивенсон', '')); $('#leafNode').show('fast');});});
			#$('#q54-No').click(function() {$('#q54').hide('fast', function() {$('#q59').show('fast');});});
		#</script>
	#],
	#[
		#'А монстров любите?'],
			#['Да'],
			#['Нет',
		#<button id="q55-Back" class="btnBack" onClick="goBack('q55', 'q50')">< Назад</button>
		#<script>
			#$('#q55-Yes').click(function() {$('#q55').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q55', '36265', 'Вокзал потерянных снов', 'Чайна Мьевиль', '')); $('#leafNode').show('fast');});});
			#$('#q55-No').click(function() {$('#q55').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q55', '33814', 'Дело Джен, или Эйра немилосердия', 'Джаспер Ффорде', '')); $('#leafNode').show('fast');});});
		#</script>
	#],
	#[
		#'Полноценная война с зомби, или одиночка против орд ходячих мервецов?'],
			#['Оба мимо'],
			#['Война'],
			#['Одиночка',
#Пожалуй, подумав, я бы предпочёл что-то классическое.
#С компанией, хоть на край света, а хоть крошить трупы.
#Я - мизантроп.
		#<button id="q56-Back" class="btnBack" onClick="goBack('q56', 'q52')">< Назад</button>
		#<script>
			#$('#q56-No').click(function() {$('#q56').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q56', '80310', 'Франкенштейн', 'Мэри Шелли', '')); $('#leafNode').show('fast');});});
			#$('#q56-war').click(function() {$('#q56').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q56', '121626', 'Мировая война Z', 'Макс Брукс', '')); $('#leafNode').show('fast');});});
			#$('#q56-oneman').click(function() {$('#q56').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q56', '18643', 'Я - легенда', 'Ричард Матесон', '')); $('#leafNode').show('fast');});});
		#</script>
	#],
	#[
		#'Любовная история или человек, преодолевающий свой интеллектуальную немощь?'],
			#['Любовная история'],
			#['Второе',

#Мне всегда было очень жалко умственно-отсталых.
		#<button id="q57-Back" class="btnBack" onClick="goBack('q57', 'q53')">< Назад</button>
		#<script>
			#$('#q57-romance').click(function() {$('#q57').hide('fast', function() {$('#q60').show('fast');});});
			#$('#q57-underdog').click(function() {$('#q57').hide('fast', function() {$('#leafNode').html(buildFinalHTML('q57', '52178', 'Цветы для Элджернона', 'Дэниел Киз', '')); $('#leafNode').show('fast');});});
		#</script>
	#],
	#[
		#'Что-то постмодернистское и психоделическое?'],
			#['Да'],
			#['Нет',
#Если кто-то начинает рассматривать нео-культурное повествование, он встаёт перед выбором: либо принять субтекстуальную парадигму выражения или придти к заключению, что повествование должно возникнуть в процессе общения. Это диалектическая парадигма содержания содержится в нём самом...

		#<button id="q58-Back" class="btnBack" onClick="goBack('q58', 'q53')">< Назад</button>
		#<script>
			#$('#q58-Yes').click(function() {$('#q58').hide('fast', function() {$('#q61').show('fast');});});
			#$('#q58-No').click(function() {$('#q58').hide('fast', function() {$('#q62').show('fast');});});
		#</script>
	#],
	[
		'Что звучит интереснее: умирающее Солнце или монстр, состоящий из колючей проволоки, лезвий, шипов и других острых предметов?',
		54,
		[
			['Умирающее Солнце. Это звучит поэтично.', '31459', 'Книга Нового Солнца', 'Джин Вулф'],
			['Монстр. Дайте мне уже Шрайка!', '1', 'Гиперион', 'Дэн Симмонс']
		]
	],
	[
		'Как насчёт путешествия во времени, сопряжённое с любовной историей?',
		57,
		[
			['Жмите. Увы и увы. Здесь не из чего больше выбирать.', 63]
		]
	],
	[
		'Может ещё небольшое путешествие во времени?',
		58,
		[
			['Да', '3799', 'Бойня номер пять', 'Курт Воннегут'],
			['Нет', '1435', 'Колыбель для кошки', 'Курт Воннегут']
		]
	],
	[
		'Как относитесь к мрачным безысходным фантазиям?',
		58,
		[
			['Давайте. Мне нравятся самые мрачные сценарии.', 64],
			['Нет, спасибо. Мир и так не сахар.', '9633', 'Скотный двор', 'Джордж Оруэлл']
		]
	],
	[
		'Классическая или современная?',
		60,
		[
			['Классическая', '145088', 'Чужестранка', 'Диана Гэблдон'],
			['Современная', '40342', 'Жена путешественника во времени', 'Одри Ниффенеггер']
		]
	],
	[
		'Тоталитарная антиутопия или мир, погружающийся в глубины безумия?',
		62,
		[
			['Диктатура', 65],
			['Сумасшествие', 66]
		]
	],
	[
		'И какая диктатура?',
		64,
		[
			['Религиозная', '54723', 'Рассказ служанки', 'Маргарет Этвуд'],
			['Военный коммунизм', '9632', '1984', 'Джордж Оруэлл']
		]
	],
	[
		'Как бы Вы отнеслись к миру, где людей изготавливают на фабриках?',
		64,
		[
			['Заинтересовало бы', '31535', 'О дивный новый мир', 'Олдос Хаксли'],
			['Не интересно', 67]
		]
	],
	[
		'Какой вопрос пугает Вас больше?',
		66,
		[
			['Книги, кому они нужны?', '5039', '451° по Фаренгейту', 'Рэй Брэдбери'],
			['Свободная воля, кому нужна?', '16230', 'Заводной апельсин', 'Энтони Бёрджесс'],
			['Никакой. Хочется чего-то более постапокалиптического.', 68]
		]
	],
	[
		'Как будто мир обратился в пепел?',
		67,
		[
			['Да. Тем более, что в истории люди, которые были готовы сжечь Землю в ядерной войне.', '140298', 'Дорога', 'Кормак Маккарти'],
			['Нет. Прикольнее было бы про пандемию почитать.', '293', 'Противостояние', 'Стивен Кинг']
		]
	],
	[
		'Но хоть как-то Вы с фэнтези знакомы?',
		6,
		[
			['Да. Это же про эльфов!', '1678', 'Сильмариллион', 'Дж. Р. Р. Толкин'],
			['Нет. У меня даже единорожье молоко на губах не обсохло.', '1693', 'Властелин Колец', 'Дж. Р. Р. Толкин']
		]
	]
]
