from peewee import *
import os.path

DIRNAME="/home/siddhantmanocha/Projects/jabongImages/"
db = PostgresqlDatabase('fashion', user='fashion', password='fashion', host='localhost')
db.connect()

 # 1) tops-tees-shirts          | 34107    
 # 2) women-sweatshirts         |  2131
 # 3) leggings-jeggings         |  3719
 # 4) capris-shorts-skirts      |  5578
 # 5) tunics                    |  2478
 # 6) sweaters                  |  2155
 # 7) trousers-jeans            |  5601
 # 8) dresses-jumpsuits-dresses | 14273
 # 9) winter-jackets            |  2724

# cat net | shuf > net1
# gawk 'BEGIN {srand()} {f = FILENAME (rand() <= 0.8 ? ".80" : ".20"); print > f}' net1
# wc -l net*


class JabongData(Model):
    id = PrimaryKeyField(primary_key=True)
    product_link = CharField()
    image_320 = CharField()
    image_500      = CharField()
    image_768      = CharField()
    image_1024     = CharField()
    image_1280     = CharField()
    brand          = CharField()
    name           = CharField()
    previous_price = CharField()
    standard_price = CharField()
    discount       = CharField()
    requestURL     = CharField()
    category       = CharField()

    class Meta:
        database=db

db.connect()


labels={
1:'tops-tees-shirts',            
2:'women-sweatshirts',     
3:'leggings-jeggings' ,        
4:'capris-shorts-skirts',      
5:'tunics',                   
6:'sweaters',                
7:'trousers-jeans' ,           
8:'dresses-jumpsuits-dresses', 
9:'winter-jackets'
}  
filename='net'

if os.path.isfile(filename):
    os.remove(filename)
    os.remove(filename+'1')
    os.remove('train.txt')
    os.remove('test.txt')

for key,val in labels.iteritems():
    print key
    complete_data = JabongData.select(JabongData.id, JabongData.product_link, JabongData.image_1280, JabongData.name, JabongData.category).where(JabongData.category==val)
    result=""
    count=0
    for row in complete_data:
        if row.image_1280:
            tmpname=row.image_1280.replace("/", "_")
            fname=DIRNAME+tmpname
            if os.path.isfile(fname):
                result+='dataset/'+tmpname+' '+str(key)+'\n'
                count+=1
    print count
    with open(filename,'a+') as f:
        f.write(result)
os.system('cat '+filename+' | shuf > '+filename+'1')
os.system("gawk 'BEGIN {srand()} {f = FILENAME (rand() <= 0.8 ? \".80\" : \".20\"); print > f}' "+filename+'1')
os.system('mv '+filename+'1.80 train.txt')
os.system('mv '+filename+'1.20 test.txt')
