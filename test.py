import requests, json, os, shutil, random
from github import Github

access_token = os.environ['MY_GITHUB_TOKEN']
service_key = os.environ['MY_SERVICE_KEY']

g = Github(access_token)
repo = g.get_user().get_repo('YOURTRIP_data')

url = 'http://apis.data.go.kr/B551011/KorService/areaBasedList?numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=AppTest&ServiceKey='+service_key+'&listYN=Y&arrange=A&contentTypeId=&areaCode=&sigunguCode=&cat1=&cat2=&cat3=&_type=json'
data = requests.get(url).json()

result = {}
area_code = { '1': '서울', '2': '인천', '3': '대전', '4': '대구', '5': '광주', '6': '부산', '7': '울산', '8': '세종특별자치시', '31': '경기도', '32': '강원도', '33': '충청북도', '34': '충청남도', '35': '경상북도', '36': '경상남도', '37': '전락북도', '38': '전라남도', '39': '제주특별자치도'}

theme_code = { '1': '야경', '2': '역사', '3': '자연', '4': '힐링', '5': '공연행사', '6': '체험', '7': '이런곳은어때요', '8': '오늘의여행지', '9': '오늘의식당', '10': '전체여행지', '11': '전체식당' }
theme_list = { 'A02050300': '1', 'A02050100': '1', 'A02050200': '1', 'A02050600': '1', 'A0201': '2', 'A01010100': '3', 'A01010200': '3', 'A01010300': '3', 'A01010500': '3', 'A01010600': '3', 'A01010700': '3', 'A0202': '4', 'A0207': '5', 'A0208': '5', 'A0203': '6', 'A02020400': '7', 'A02030400': '7', 'A02030600': '7', 'A05020700' : '7' }
# A0302': '4', 'A0303': '4', 'A0304': '4', 'A0305': '4'

detail_code = { 'A01010100': '국립공원', 'A01010200': '도립공원', 'A01010300': '군립공원', 'A01010400': '산', 'A01010500': '자연생태관광지', 'A01010600': '자연휴양림', 'A01010700': '수목원', 'A01010800': '폭포', 'A01010900': '계곡', 'A01011000': '약수터', 'A01011100': '해안절경', 'A01011200': '해수욕장', 'A01011300': '섬', 'A01011400': '항구/포구', 'A01011500': '어촌', 'A01011600': '등대', 'A01011700': '호수', 'A01011800': '강', 'A01011900': '동굴', 'A01020100': '희귀동.식물', 'A01020200': '기암괴석', 'A02010100': '고궁', 'A02010200': '성', 'A02010300': '문', 'A02010400': '고택', 'A02010500': '생가', 'A02010600': '민속마을', 'A02010700': '유적지/사적지', 'A02010800': '사찰', 'A02010900': '종교성지', 'A02011000': '안보관광', 'A02020100': '유원지', 'A02020200': '관광단지', 'A02020300': '온천/욕장/스파', 'A02020400': '이색찜질방', 'A02020500': '헬스투어', 'A02020600': '테마공원', 'A02020700': '공원', 'A02020800': '유람선/잠수함관광', 'A02030100': '농.산.어촌 체험', 'A02030200': '전통체험', 'A02030300': '산사체험', 'A02030400': '이색체험', 'A02030500': '관광농원', 'A02030600': '이색거리', 'A02050100': '다리/대교', 'A02050200': '기념탑/기념비/전망대', 'A02050300': '분수', 'A02050400': '동상', 'A02050500': '터널', 'A02050600': '유명건물', 'A02060100': '박물관', 'A02060200': '기념관', 'A02060300': '전시관', 'A02060400': '컨벤션센터', 'A02060500': '미술관/화랑', 'A02060600': '공연장', 'A02060700': '문화원', 'A02060800': '외국문화원', 'A02060900': '도서관', 'A02061000': '대형서점', 'A02061100': '문화전수시설', 'A02061200': '영화관', 'A02061300': '어학당', 'A02061400': '학교', 'A02070100': '문화관광축제', 'A02070200': '일반축제', 'A02080100': '전통공연', 'A02080200': '연극', 'A02080300': '뮤지컬', 'A02080400': '오페라', 'A02080500': '전시회', 'A02080600': '박람회', 'A02080700': '컨벤션', 'A02080800': '무용', 'A02080900': '클래식음악회', 'A02081000': '대중콘서트', 'A02081100': '영화', 'A02081200': '스포츠경기', 'A02081300': '기타행사', 'A05020100': '한식', 'A05020200': '서양식', 'A05020300': '일식', 'A05020400': '중식', 'A05020500': '아시아식', 'A05020600': '패밀리레스토랑', 'A05020700': '이색음식점', 'A05020800': '채식전문점', 'A05020900': '바/까페', 'A05021000	': '클럽' }

necessary_keys = ['addr1', 'contentid', 'firstimage', 'firstimage2', 'mapx', 'mapy', 'readcount', 'title']

for item in data['response']['body']['items']['item']:
    if not item['areacode']:
        continue

    if not item['firstimage'] or not item['firstimage2']:
        continue

    if item['contenttypeid'] in ['14', '25', '28', '32', '38'] or not item['contenttypeid']:
        continue

    if item['cat2'] in ['A0102', 'A0204'] or not item['cat2']:
        continue

    if item['cat3'] in ['A01010400', 'A01010900', 'A01011000', 'A01011400', 'A01011500'] or not item['cat3']:
        continue

    if item['cat3'] not in detail_code:
        continue

    area = result.get('area', {})
    area_string = area_code[item['areacode']]
    area_data = area.get(area_string, {})

    def createNewData():
        new_data = {}

        for k in item:
            if k in necessary_keys:
                new_data[k] = item[k]

        new_data['detail'] = detail_code[item['cat3']]
        new_data['desc'] = 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Possimus magni voluptates distinctio vero sit est sed placeat, odit accusantium! Reprehenderit rerum dolorem consectetur assumenda voluptatum. Odit eveniet tempore reiciendis repellendus. Tempore esse mollitia et perferendis omnis magni pariatur temporibus? Quos consequatur unde odit assumenda deleniti iste dolor, impedit molestias perspiciatis. Illum, molestias pariatur adipisci aut commodi eaque praesentium et delectus! Nam repellendus dolorem maiores, distinctio illum non eos vel quam quidem commodi minima autem doloremque voluptate saepe, expedita molestias repellat magni iste in ad delectus. Earum maxime officia ea vitae.'

        return new_data

    def addData(theme):
        new_data = createNewData()

        theme_data = area_data.get(theme, {})
        theme_data_list = theme_data.get('list', [])
        theme_data_list.append(new_data)
        theme_data['list'] = theme_data_list

        theme_data['count'] = theme_data.get('count', 0) + 1

        area_data[theme] = theme_data

    if item['cat2'] in theme_list:
        addData(theme_code[theme_list[item['cat2']]])

    if item['cat3'] in theme_list:
        addData(theme_code[theme_list[item['cat3']]])

    if item['cat1'] == 'A05':
        addData(theme_code['11'])
    else:
        addData(theme_code['10'])

    area_data['count'] = area_data.get('count', 0) + 1

    area[area_string] = area_data
    result['area'] = area


    ########### new category
    today = result.get('today', {})

    if random.randrange(1, 1001) < 5:
        today_list = today.get('list', [])
        new_data = createNewData()
        today_list.append(new_data)
        today['list'] = today_list

        today['count'] = today.get('count', 0) + 1

    result['today'] = today

for area in result['area']:
    image_list = []

    for theme in result['area'][area]:
        if theme != 'count':
            result['area'][area][theme]['image'] = random.choice(list(result['area'][area][theme]['list']))['firstimage']
            image_list.append(result['area'][area][theme]['image'])

    result['area'][area]['image'] = random.choice(image_list)

for category in result:
    if not result[category].get('list', ''):
        continue

    result[category]['image'] = random.choice(list(result[category]['list']))['firstimage']

try:
  contents = repo.get_contents("data.json")
  print('find file')
  repo.delete_file(contents.path, "remove data", contents.sha, branch="main")
  print('recreate file')
  repo.create_file('data.json', 'update 여행지 데이터', json.dumps(result, indent=4, ensure_ascii=False), branch='main')
except:
  print('create file')
  repo.create_file('data.json', 'create 여행지 데이터', json.dumps(result, indent=4, ensure_ascii=False), branch='main')
