import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 600
kakudo = 0
key = {
    pg.K_UP:(0,+5),
    pg.K_DOWN:(0,-5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}

def kk_key_k():
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img_s = pg.transform.flip(kk_img,True,False)
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    return {
            (0,0):pg.transform.flip(kk_img,True,False),
            (0,-5):pg.transform.rotozoom(kk_img,270,1.0),
            (-5,-5):pg.transform.rotozoom(kk_img,315,1.0),
            (-5,0):pg.transform.rotozoom(kk_img,0,1.0),
            (-5,+5):pg.transform.rotozoom(kk_img,45,1.0),
            (0,+5):pg.transform.rotozoom(kk_img,90,1.0),
            (+5,+5):pg.transform.rotozoom(kk_img_s,315,2.0),
            (+5,0):pg.transform.flip(kk_img,True,False),
            (+5,-5):pg.transform.rotozoom(kk_img_s,45,2.0)
            } #こうかとんの画像の角度の向きがそれぞれ違う画像の辞書
        
       
def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    オブジェクトが画面内or画面外を判定し、真理値タプルを返す関数
    引数 rct：こうかとんor爆弾SurfaceのRect
    戻り値：横方向，縦方向はみ出し判定結果（画面内：True／画面外：False）
    """
    yoko,tate = True,True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_key_lst = kk_key_k()
    kk_img = kk_key_lst[(0,0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900,400
    bom = pg.Surface((20,20))
    pg.draw.circle(bom,(255,0,0),(10,10),10)
    bom.set_colorkey((0,0,0))
    bom_rct = bom.get_rect()
    bom_rct.centerx = random.randint(0,WIDTH)
    bom_rct.centery = random.randint(0,HEIGHT)
    vx,vy = +5,+5

    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        if kk_rct.colliderect(bom_rct):
            bg_img_si = pg.image.load("ex02/fig/pg.11.png")
            bg_img_sis = pg.transform.rotozoom(bg_img_si,0,3.0)
            screen.blit(bg_img_sis, [0, 0])
            pg.display.update()
            clock.tick(0.5)
            print("Game Over")
            return #あたったときに、画面を切り替える

        key_lst = pg.key.get_pressed()
        sum_mv = [0,0]
        for k,tpi in key.items():
            if key_lst[k]:
                sum_mv[0] += tpi[0]
                sum_mv[1] -= tpi[1]

        

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0],sum_mv[1])
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        kk_img = kk_key_lst[tuple(sum_mv)]#型を合わせた
        
        screen.blit(kk_img, kk_rct)
        bom_rct.move_ip(vx,vy)
        yoko, tate = check_bound(bom_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bom_rct.move_ip(vx,vy)
        screen.blit(bom,bom_rct)
        pg.display.update() #画像のアップデート
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()