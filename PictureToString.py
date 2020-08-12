from PIL import Image
import os
import json
import pygame
class CharacterDrawing():
    def __init__(self,**kw):
        self.ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
        # self.input_file=kw["input_file"]
        # self.width = kw["width"]
        # self.height = kw["height"]
        # self.output_file = kw["output_file"]
        self.text_names=[]
        self.coefficient=""
        self.columns=""
        self.input_picture_names=[]
        self.gen_file_name = "生成字符画"
        self.prepare()

    def transform(self):
        #打开图片
        for picture_name in self.input_picture_names:
            im = Image.open(picture_name)
            original_width=im.size[0]
            original_height=im.size[1]
            print(im.size)
            text_width=int(self.columns)
            text_height=int(text_width*original_height/original_width)
            im = im.resize((text_width, text_height), Image.BOX)
            #im=im.resize((text_width, text_height), Image.NEAREST)
            self.put_row_text(picture_name,im,text_width,text_height)

    def put_row_text(self,picture_name,im,width,height):
        width,height=int(width),int(height)
        print(width, height)


        txt = ""
        for i in range(height):
            for j in range(width):
                txt += self.get_char(*im.getpixel((j, i)))
            txt += '\n'
        file_name= picture_name.split(".")[0]+"gen"+".txt"
        self.text_names.append(file_name)
        print(file_name)
        with open(self.gen_file_name+'/'+file_name, "w") as f:
            f.write(txt)

    def get_char(self,r,g,b,alpha = 256):
        if alpha == 0:
            return ' '
        length = len(self.ascii_char)
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

        unit = (256.0 + 1) / length
        return self.ascii_char[int(gray / unit)]
    def prepare(self):
        #创建生成目录
        if not os.path.exists(self.gen_file_name):
            os.mkdir(self.gen_file_name)

        if not os.path.exists("./说明.txt"):
            with open("说明.txt", "w",encoding="UTF-8") as f:
                text="操作步骤:\n"+"将图片放到PictureToString.exe所在的文件夹，然后点击PictureToString.exe，即可在’生成字符画’文件夹下生成txt文件"+"打开txt文件，按住ctrl+鼠标滚轮缩放\n"+"点击格式-字体-选择宋体 效果会更好\n"
                text=text+"打开config.json文件，其中columns对应的数字，就是生成的txt文件每一行的列数,可以自行修改，比如改成{‘coefficient’: 1, ‘columns’: 30}，就是每一行只有三十个字符\n"
                f.write(text)
        #创建并生成配置文件
        if not os.path.exists("./config.json"):
            with open("config.json", "w") as f:
                dict = {}
                dict["coefficient"] = 1  # 缩放系数
                dict["columns"] = 300  # 每一行多少个字符，默认300个
                print(json.dumps(dict))
                f.write(json.dumps(dict))
        with open("config.json", "r") as f:
            dict = json.loads(f.read())
            self.coefficient=dict["coefficient"]
            self.columns=dict["columns"]

        #获取本目录下所有图片
        currentDir = os.getcwd()
        picturesDir = a = os.listdir(currentDir)
        for i in picturesDir:
            if i.split('.')[-1] in ("jpeg", "jpg", "png"):
                self.input_picture_names.append(i)
    # def toPicture(self):
    #     pygame.init()
    #     for i in self.text_names:
    #         with open(self.gen_file_name+'/'+i,"r") as f:
    #             text=f.read()
    #             print(text)
    #             font = pygame.font.SysFont('SimSun', 64)
    #             ftext = font.render(text, True, (0, 0, 0), (255, 255, 255))
    #             pygame.image.save(ftext, self.gen_file_name+'/'+i.split(".")[0]+".jpg")


if __name__=="__main__":
    draw= CharacterDrawing(input_file="hls.jpg",width=248,height=373,output_file="1.txt")
    draw.transform()
    # draw.toPicture()
