daftar_jurus = {'naga kacang':'nagakacang.txt'}
daftar_cmd = ['bye', 'gombal', 'help', 'info', 'jurus', 'tag', 'taglist', 'ougi', 'panggil', 'profil', 'so']
daftar_tag = ['gagal ambis','gagal ambis','alone','disgusting','jalan setan','jaga ketikan','kok sepi','matte','mecin','moshi','mwhaha','nani','NO','NOOO','pintar',
              'rasenggan','savage','sepi','weewoo','yamete','otak dengkul']
img_url = { 'bye':['https://image.ibb.co/ibvkKa/akatsukileave.jpg','https://image.ibb.co/meYGQF/akatsukileave_prev.jpg'],
            'gagal ambis':['https://image.ibb.co/hH2Msv/gagal_ngambis.jpg','https://image.ibb.co/mkb35F/gagal_ngambis_prev.jpg'],
            'alone':['https://image.ibb.co/g9OHhv/alone_prev.jpg','https://image.ibb.co/cahopa/disgusting.jpg'],
            'disgusting':['https://image.ibb.co/gaREUa/disgusting_prev.jpg','https://image.ibb.co/hPE19a/hai.jpg'],
            'jalan setan':['https://image.ibb.co/mPCA2v/jalansetan.jpg','https://image.ibb.co/eEiTpa/jalansetan_prev.jpg'],
            'jaga ketikan':['https://image.ibb.co/jsGRaF/ketikandijaga.jpg','https://image.ibb.co/e3vKvF/ketikandijaga_prev.jpg'],
            'kok sepi':['https://image.ibb.co/hViiNv/koksepi.jpg','https://image.ibb.co/dWHA2v/koksepi_prev.jpg'],
            'matte':['https://image.ibb.co/bXmsFF/matte.jpg','https://image.ibb.co/faLmaF/matte_prev.jpg'],
            'mecin':['https://image.ibb.co/iMUCFF/mecin.jpg','https://image.ibb.co/djJiNv/mecin_prev.jpg'],
            'moshi':['https://image.ibb.co/mbkmaF/moshi.jpg','https://image.ibb.co/i2Copa/moshi_prev.jpg'],
            'mwhaha':['https://image.ibb.co/cdwEUa/mwahaha.jpg','https://image.ibb.co/bOMEUa/mwahaha_prev.jpg'],
            'nani':['https://image.ibb.co/eNbg9a/nani.jpg','https://image.ibb.co/moA8pa/nani_prev.jpg'],
            'NO':['https://image.ibb.co/bSDiNv/NO.jpg','https://image.ibb.co/jgrEUa/NO_prev.jpg'],
            'NOOO':['https://image.ibb.co/dtschv/NOOO.jpg','https://image.ibb.co/dtschv/NOOO.jpg'],
            'pintar':['https://image.ibb.co/kOnShv/pintar.jpg', 'https://image.ibb.co/iFhGaF/pintar_prev.jpg'],
            'rasenggan':['https://image.ibb.co/kSQDNv/rasenggan.jpg','https://image.ibb.co/ciV2FF/rasenggan_prev.jpg'],
            'savage':['https://image.ibb.co/egn4Ua/savage.jpg','https://image.ibb.co/bDPUvF/savage_Copy.jpg'],
            'sepi':['https://image.ibb.co/k8CShv/sepi.jpg','https://image.ibb.co/hp802v/sepi_prev.jpg'],
            'weewoo':['https://image.ibb.co/jmejUa/weewoo.jpg','https://image.ibb.co/hrStNv/weewoo_prev.jpg'],
            'yamete':['https://image.ibb.co/fMADNv/yamete.jpg','https://image.ibb.co/fMADNv/yamete.jpg'],
            'otak dengkul':['https://image.ibb.co/dngEUa/otakdengkul.jpg','https://image.ibb.co/kuEUvF/otakdengkul_prev.jpg'],
           }
f = open('statics/gombal.txt', 'r')
list_gombal = (f.read()).splitlines()
f.close()
