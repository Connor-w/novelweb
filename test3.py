import os
import os
path = r'/Users/macos/Desktop/connorshare/media/section_content'
if not os.path.exists(r'./media/section_content'+'/最强桃运系统'):
    path = r'./media/section_content'
    os.mkdir(path +'/最强桃运系统')
with open('./media/section_content/最强桃运系统/1212.text','w') as f:
    f.write('1')