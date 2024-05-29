import sys

from workflow import Workflow

class ICON(object):
    DEFAULT = 'icon.png'
    SOUND = 'sound.png'

def main():
    text = sys.argv[1]
    wf = Workflow()

    wf.add_item(
        title=text,
        subtitle=u"查询 " + text,
        valid=True,
        arg=text,
        icon=ICON.DEFAULT
    )

    wf.send_feedback()

if __name__ == u"__main__":
    main()
