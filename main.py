import pygame, os, sys

pygame.init()

W, H = 420, 780
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("WriterPro")

BG = (18,18,24)
WHITE = (245,245,245)
GRAY = (160,160,170)
BOX = (35,35,45)
BLUE = (45,110,200)
GREEN = (55,160,90)
PURPLE = (110,90,180)
RED = (180,70,70)

title_font = pygame.font.Font(None,42)
font = pygame.font.Font(None,28)
small = pygame.font.Font(None,21)

title = ""
article = ""
keyword = ""
active = None
scroll = 0
show_results = False
show_files = False
message = ""

folder = "/storage/emulated/0/WriterPro_Articles"

pygame.key.start_text_input()


def text(value,x,y,f=font,c=WHITE):
    screen.blit(f.render(str(value),True,c),(x,y))


def box(rect,selected=False):
    pygame.draw.rect(
        screen,
        BLUE if selected else BOX,
        rect,
        border_radius=8
    )


def lines(text_value):
    result=[]

    for paragraph in text_value.split("\n"):
        line=""

        for word in paragraph.split():
            test=line+word+" "

            if font.size(test)[0] <= 350:
                line=test
            else:
                result.append(line)
                line=word+" "

        if line:
            result.append(line)

        result.append("")

    return result


def new_article():
    global title,article,keyword,scroll,show_results,message

    title=""
    article=""
    keyword=""
    scroll=0
    show_results=False
    message=""


def save_article():
    global message

    if not article.strip():
        message="Write an article first."
        return

    try:
        os.makedirs(folder,exist_ok=True)

        name=title.strip() or "Untitled_Article"

        safe=""
        for c in name:
            if c.isalnum() or c in " -_":
                safe+=c

        safe=safe or "Untitled_Article"

        path=os.path.join(folder,safe+".txt")

        with open(path,"w",encoding="utf-8") as f:
            f.write(title+"\n\n"+article)

        message="Article saved!"

    except:
        message="Save failed."


def get_files():
    try:
        os.makedirs(folder,exist_ok=True)

        return sorted(
            f for f in os.listdir(folder)
            if f.endswith(".txt")
        )

    except:
        return []


def load_article(filename):
    global title,article,keyword
    global show_files,message,scroll

    try:
        path=os.path.join(folder,filename)

        with open(path,"r",encoding="utf-8") as f:
            data=f.read()

        parts=data.split("\n\n",1)

        title=parts[0]
        article=parts[1] if len(parts)>1 else ""

        keyword=""
        scroll=0
        show_files=False
        message="Article loaded!"

    except:
        message="Could not load article."


def analyze():
    global show_results,message

    words=article.split()
    count=len(words)

    key=keyword.strip().lower()

    hits=article.lower().count(key) if key else 0

    density=(hits/count*100) if count else 0

    score=0

    if count>=300:
        score+=30
    elif count>=100:
        score+=20
    elif count:
        score+=10

    if key and hits:
        score+=30

    if hits>=2:
        score+=20

    if count:
        score+=20

    reading=max(1,round(count/200)) if count else 0

    message=(
        f"SEO: {score}/100 | "
        f"Words: {count} | "
        f"Keyword: {hits} | "
        f"Density: {density:.1f}% | "
        f"Reading: {reading} min"
    )

    show_results=True


running=True

while running:

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            running=False

        elif event.type==pygame.MOUSEBUTTONDOWN:

            x,y=event.pos

            # FILE SCREEN
            if show_files:

                if pygame.Rect(20,720,380,45).collidepoint(x,y):
                    show_files=False

                else:
                    for i,name in enumerate(get_files()):

                        r=pygame.Rect(20,150+i*55,380,45)

                        if r.collidepoint(x,y):
                            load_article(name)
                            break

            # ARTICLE
            elif pygame.Rect(20,210,380,250).collidepoint(x,y):

                active="article"

            # TITLE
            elif pygame.Rect(20,120,380,55).collidepoint(x,y):

                active="title"

            # KEYWORD
            elif pygame.Rect(20,530,380,55).collidepoint(x,y):

                active="keyword"

            # NEW
            elif pygame.Rect(15,600,95,60).collidepoint(x,y):

                new_article()

            # LOAD
            elif pygame.Rect(115,600,95,60).collidepoint(x,y):

                show_files=True

            # SAVE
            elif pygame.Rect(215,600,95,60).collidepoint(x,y):

                save_article()

            # ANALYZE
            elif pygame.Rect(315,600,90,60).collidepoint(x,y):

                analyze()

            else:
                active=None

        elif event.type==pygame.TEXTINPUT:

            if active=="title":
                title+=event.text

            elif active=="article":
                article+=event.text

            elif active=="keyword":
                keyword+=event.text

        elif event.type==pygame.KEYDOWN:

            if event.key==pygame.K_BACKSPACE:

                if active=="title":
                    title=title[:-1]

                elif active=="article":
                    article=article[:-1]

                elif active=="keyword":
                    keyword=keyword[:-1]

            elif event.key==pygame.K_RETURN:

                if active=="article":
                    article+="\n"

        elif event.type==pygame.MOUSEWHEEL:

            if active=="article":
                scroll+=event.y*30

    # DRAW

    screen.fill(BG)

    if show_files:

        text("MY ARTICLES",120,45,title_font)

        files=get_files()

        if not files:
            text("No saved articles yet.",105,150,small,GRAY)

        for i,name in enumerate(files[:9]):

            y=150+i*55
            box(pygame.Rect(20,y,380,45))
            text(name[:-4][:30],30,y+10,small)

        pygame.draw.rect(
            screen,RED,(20,720,380,45),
            border_radius=8
        )

        text("BACK",180,731,small)

        pygame.display.flip()
        continue

    text("WRITERPRO",125,35,title_font)
    text(
        "Professional Writing Assistant",
        85,80,small,GRAY
    )

    text("Article Title",20,100,small,GRAY)

    r=pygame.Rect(20,120,380,55)
    box(r,active=="title")

    text(title or "Tap and type...",30,135,font,
         WHITE if title else GRAY)

    text("Article",20,190,small,GRAY)

    r=pygame.Rect(20,210,380,250)
    box(r,active=="article")

    old=screen.get_clip()
    screen.set_clip(r)

    if article:

        y=220+scroll

        for line in lines(article):

            if 210<=y<460:
                text(line,30,y)

            y+=30

    else:
        text("Tap and type...",30,225,font,GRAY)

    screen.set_clip(old)

    text(f"Words: {len(article.split())}",20,475,small)
    text(f"Characters: {len(article)}",170,475,small)

    text("Main Keyword",20,505,small,GRAY)

    r=pygame.Rect(20,530,380,55)
    box(r,active=="keyword")

    text(keyword or "Tap and type...",30,545,font,
         WHITE if keyword else GRAY)

    buttons=[
        ("NEW",15,GRAY),
        ("LOAD",115,PURPLE),
        ("SAVE",215,GREEN),
        ("ANALYZE",315,BLUE)
    ]

    for name,x,color in buttons:

        width=95 if name!="ANALYZE" else 90

        pygame.draw.rect(
            screen,color,
            (x,600,width,60),
            border_radius=10
        )

        text(name,x+12,620,small)

    if show_results or message:
        text(message,20,725,small)

    pygame.display.flip()

pygame.key.stop_text_input()
pygame.quit()
sys.exit()