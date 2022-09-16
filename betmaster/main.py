# 11th September, 2022
# Amoh-Gyebi Ampofo

from ast import main
from summary_functions import main_summary

# home = 'olympiakos'
# away = 'freiburg'
# home = 'trabzonspor'
# away = 'crvena-zvezd'
""" matches = [
    ('as-monaco', 'ferencvaros'), ('olympiakos', 'freiburg'), ('ps-tni', 'pss-sleman'),
    ('trabzonspor', 'crvena-zvezd'), ('qarabag-agdam', 'fc-nantes'),
    ('fc-midtjylland', 'lazio'), ('feyenoord', 'sturm-graz'),
    ('real-sociedad', 'omonia-nicosia'), ('sheriff-tiraspol', 'manchester-united'),
    ('sporting-braga', 'union-berlin'), ('union-saint-gilloise', 'malmo-ff'),
    ('as-roma', 'hjk-helsinki'), ('real-betis', 'ludogorets-razgrad'),
    ('bodo-glimt', 'fc-zurich'), ('dynamo-kiev', 'aek-larnaca'),
    ('stade-rennais', 'fenerbahce'), ('sandecja-nowy-sacz', 'stal-rzeszow'),
    ('aris-limassol', 'karmiotissa-pano-polemidia'), ('gandzasar-ii', 'mika-fc'),
    ('usk-anif', 'st-polten-spratzern'), ('hamburger-sv-ii', 'vfb-lubeck'),
    ('hapoel-afula', 'bnei-yehuda'), ('hapoel-petah-tikva', 'agudat-sport-ashdod')] """


""" matches = [
    ('as-monaco', 'ferencvaros'), ('olympiakos', 'freiburg'),
    ('trabzonspor', 'crvena-zvezd'), ('qarabag-agdam', 'fc-nantes'),
    ('fc-midtjylland', 'lazio'), ('feyenoord', 'sturm-graz'),
    ('real-sociedad', 'omonia-nicosia'), ('sheriff-tiraspol', 'manchester-united'),
    ('sporting-braga', 'union-berlin'), ('union-saint-gilloise', 'malmo-ff'),
    ('as-roma', 'hjk-helsinki'), ('real-betis', 'ludogorets-razgrad'),
    ('bodo-glimt', 'fc-zurich'), ('dynamo-kiev', 'aek-larnaca'),
    ('stade-rennais', 'fenerbahce'), ('sandecja-nowy-sacz', 'stal-rzeszow'),
    ('aris-limassol', 'karmiotissa-pano-polemidia'), ('gandzasar-ii', 'mika-fc'),
    ('usk-anif', 'st-polten-spratzern'), ('hamburger-sv-ii', 'vfb-lubeck'),
    ('hapoel-afula', 'bnei-yehuda'), ('hapoel-petah-tikva', 'agudat-sport-ashdod'),
    ('hapoel-ramat-gan', 'maccabi-petah-tikva'), ('hapoel-umm-al-fahm', 'hapoel-kfar-saba'),
    ('ironi-nir-ramat-hasharon', 'hapoel-nof-hagalil'), ('fc-giugliano-1928', 'az-picerno'),
    ('foggia-calcio', 'virtus-francavilla-calcio'), ('hapoel-kfar-shalem', 'maccabi-ironi-ashdod'),
    ('dukagjini', 'drenica-skenderaj'), ('kf-trepca-89', 'ferizaj'), ('cs-aerostar-bacau', 'miercurea-ciuc'),
    ('mladost-dg', 'fk-berane'), ('varbergs-gif-fk', 'landvetter-is'),
    ('nigde-belediyespor', 'kahramanmarasspor'), ('nevsehirspor-gk', 'yozgatspor'),
    ('catalcaspor', 'edirnespor-genclik'), ('ps-tni', 'pss-sleman'),
    ('persis-solo-fc', 'bali-united'), ('fc-atyrau', 'fk-arys'),
    ('shakhter-karagandy', 'kaspiy-aktau'), ('aksu', 'akzhayik-uralsk'),
    ('kairat-almaty', 'ordabasy'), ('fk-makhtaaral', 'fk-kyzylzhar-petropavlovsk'),
    ('al-jahra-sc', 'al-qadsia-sc'), ('kazma-sc', 'al-nasr-sc'),
    ('bengaluru-fc', 'hyderabad-fc'), ('melaka-united', 'kuala-lumpur-fa'),
    ('misc-football', 'johor-darul-takzim'), ('al-baten-club', 'al-nasr-riyadh'),
    ('ajman-club', 'al-sharjah-scc'), ('al-wasl-fc-dubai', 'dibba-al-fujairah'),
    ('al-khaleej-khor-fakkan', 'al-nasr-dubai-sc'), ('al-jazira-club-abu-dhabi', 'al-ain-fc'),
    ('olmaliq-fk', 'pakhtakor-tashkent'), ('olympic-fk-tashkent', 'fc-bunyodkor'),
    ('olympic-fk-tashkent', 'fc-bunyodkor'), ('deportes-magallanes', 'santiago-morning'),
    ('cs-cerrito', 'atletico-fenix'), ('espoir-fc', 'mukura-victory-sports'),
    ('depor-fc', 'real-cartagena'), ('spartak-moscow', 'fakel-voronezh'),
    ('mps-atletico-malmi', 'hifk-ii'), ('pyunik', 'slovan-bratislava'),
    ('zalgiris-vilnius', 'fc-basel'), ('cfr-cluj', 'sivasspor'),
    ('slavia-prague', 'ballkani'), ('djurgardens-if', 'molde-fk'),
    ('kaa-gent', 'shamrock-rovers'), ('az-alkmaar', 'fc-vaduz')] """

matches = [
    ('cd-olimpia', 'diriangen-fc'),
    ('fk-rostov-u19', 'fc-chertanovo-moscow-u20'),
    ('beijing-bsu', 'nantong-zhiyun-fc'),
    ('shenyang-urban-fc', 'chongqing-lifan'),
    ('persib-bandung', 'barito-putera'),
    ('correcaminos-uat', 'dorados-de-sinaloa')]

for x in matches:
    try:
        home = x[0]
        away = x[1]
        one = main_summary(home, away)
    except:
        one = 'Error while processing'

    print(f'\n{home} vs {away} : {one}\n')
