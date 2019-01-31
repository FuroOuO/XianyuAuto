import uiautomator2 as u2
from time import sleep,time
from math import ceil
class XianYu():
    def save_g(self):
        self.d(text=u"确认发布", className="android.view.View").click()
        while len(self.d(description=u"发布成功", className="android.view.View")) == 0:
            pass
        print('>>> 后退')
        self.d.press('back')
        while True:
            if len(self.d(text=u"签到", className="android.widget.TextView")) == 1:
                # 第一种情况：进入了地区界面
                print('>>> 后退至商品列表界面')
                self.d.press('back')
                break
            elif len(self.d(text=u"收藏", className="android.widget.ImageView")) == 1:
                # 第二种情况：进入了帖子界面
                print('>>> 后退商品列表界面')
                self.d.press('back')
                break

        while len(self.d(description=u"编辑")) == 0:
            pass

        print('>>> 后退至主界面')
        self.d.press('back')
        self.good += 1
        print('>>> 完成第 %s 个商品的编辑' % self.good)
        # 计时
        self.btime = int(time())
        self.ctime = self.btime - self.atime
        print('[用时 %s 秒]' % self.ctime)

    def get_gm(self):
        if self.d(resourceId="com.taobao.idlefish:id/entry_title", text=u"我发布的"):
            # 获取发布的商品数量
            self.goods = int(self.d(resourceId="com.taobao.idlefish:id/entry_sub_title", className="android.widget.TextView",
                          instance=1).get_text())
            print('>>> 发布的商品数量：', self.goods)

    def get_g(self):
        # 计时
        self.atime = int(time())
        # 点击'我发布的'按钮
        print('>>> 点击[我发布的]')
        self.d(resourceId="com.taobao.idlefish:id/entry_title", text=u"我发布的").click()

        # 检测页面加载情况
        while len(self.d(description=u"编辑", className="android.view.View")) == 0:
            pass
        sleep(0.5)
        # 移到最底端
        print('>>> 移动到最底端')
        for i in range(0,ceil(self.goods/20)):
            # 每一次加载20个商品，滑到目前底端才会加载后20个商品
            self.d.swipe(0.5, 0.9, 0.5, 0.065, 0.01)
            sleep(2.5)

        a = len(self.d(description=u"编辑")) - 1  # 屏幕上有多少个编辑按钮

        if a == 0:
            # 点击0号'编辑'按钮(鉴于只有一个商品的情况)
            print('>>> 点击[编辑]')
            self.d(description=u"编辑", className="android.view.View").click()

        else:
            # 点击a号'编辑'按钮(最后一个'编辑'那妞)
            print('>>> 点击[编辑]')
            self.d(description=u"编辑", className="android.view.View", instance=a).click()

        self.save_g()

    def __init__(self):
        # 主循环
        self.d = u2.connect('3e9caa939804')
        print('>>> 开始一轮循环')
        # 解锁
        self.d.unlock()
        self.d.press('home')
        self.state = 0
        self.good = 0
        xianyu = len(self.d(resourceId="com.miui.home:id/icon_title", text=u"闲鱼", className="android.widget.TextView"))
        if xianyu == 0:
            sleep(1)
            self.d.press('home')
            xianyu = len(
                self.d(resourceId="com.miui.home:id/icon_title", text=u"闲鱼", className="android.widget.TextView"))
            if xianyu == 0:
                print('* 未检测到首页存在闲鱼APP，请将闲鱼APP放置在首页 *')

        print('[首页共有 %s 个咸鱼]' % xianyu)
        for xy in range(0,xianyu):
            # 打开首页咸鱼
            print('>>> 打开第 %s 个"闲鱼"APP' % (xy+1))
            if xy == 0:
                self.d(resourceId="com.miui.home:id/icon_title", text=u"闲鱼", className="android.widget.TextView").click()
            else:
                self.d(resourceId="com.miui.home:id/icon_title", text=u"闲鱼",className="android.widget.TextView",
                       instance=xy).click()

            self.d(resourceId="com.taobao.idlefish:id/tab_title", text=u"我的", className="android.widget.TextView").click()

            # 获取商品数量
            self.get_gm()

            # 循环编辑商品
            while self.good != self.goods:
                self.get_g()

            # 执行完毕
            self.good = 0
            self.d.press('back')
            self.d.press('home')

        print('>>> 全部完成')

if __name__ == '__main__':
    XianYu()