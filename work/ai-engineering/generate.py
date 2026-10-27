from pathlib import Path
import xml.etree.ElementTree as E
out=Path('public/diagrams/ai-engineering');out.mkdir(parents=True,exist_ok=True)
f=E.Element('mxfile',host='app.diagrams.net');d=E.SubElement(f,'diagram',id='overview',name='AI 研发体系')
g=E.SubElement(d,'mxGraphModel',page='1',pageWidth='1200',pageHeight='890',background='#ffffff')
r=E.SubElement(g,'root');E.SubElement(r,'mxCell',id='0');E.SubElement(r,'mxCell',id='1',parent='0')
def box(i,t,x,y,w,h,c='#eff6ff',size=20,bold=False,dark=False):
 s=f'rounded=1;arcSize=8;whiteSpace=wrap;html=0;fillColor={c};strokeColor=#cbd5e1;fontColor={"#ffffff" if dark else "#172b4d"};fontSize={size};fontFamily=Arial;spacing=14;fontStyle={1 if bold else 0};'
 a=E.SubElement(r,'mxCell',id=i,value=t,vertex='1',parent='1',style=s);E.SubElement(a,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
def edge(i,source,target,dash=False,extra=''):
 c=E.SubElement(r,'mxCell',id=i,source=source,target=target,edge='1',parent='1',style=f'edgeStyle=orthogonalEdgeStyle;endArrow=block;strokeWidth=2;strokeColor={"#0f766e" if dash else "#64748b"};dashed={int(dash)};'+extra);E.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
box('title','AI 研发体系\n编码任务 → 研发组织 → 交付闭环 → 平台承载',30,25,1140,95,'#172b4d',28,True,True)
box('legend','阅读与建设路径：前两步扩展关注范围，最后一步切换到平台承载视角。\n不是固定成熟度等级；各主题可以同时存在、相互反馈。',30,140,1140,75,'#f8fafc',20)
box('coding','01  AI coding\n\n怎样做好编码任务？\n\n上下文 · 任务拆分\n实现 · 诊断\n测试 · 审阅\n\n关注：可检查的变更',30,260,255,255,'#eff6ff',21)
box('native','02  AI Native\n\n怎样组织持续研发？\n\n人机分工 · 契约\n工程结构 · 知识\n质量 · 团队协作\n\n关注：研发条件',325,260,255,255,'#f0fdfa',21)
box('delivery','03  AI 自交付\n\n怎样形成交付闭环？\n\n目标 · 验收 · 授权\n阶段协作 · 证据\n反馈 · 完成边界\n\n关注：交付责任',620,260,255,255,'#fff7e6',21)
box('platform','04  AI 研发\nAgent 平台\n\n怎样统一承载与治理？\n\n项目 · 任务 · 能力\n上下文 · 工具 · 证据\n\n关注：组织与追溯',915,260,255,255,'#f5f3ff',21)
edge('read1','coding','native');edge('read2','native','delivery');edge('read3','delivery','platform')
box('support','平台可以承载前三类工作，不要求先完成前三步再建设。\n没有统一平台也可组织交付；拥有平台不代表编码正确、交付可靠或价值实现。',30,605,1140,90,'#f0fdfa',21)
edge('carrier','platform','support',True,'exitX=0.5;exitY=1;entryX=0.89;entryY=0;')
for i,x in [('coding',0.11),('native',0.37),('delivery',0.63)]:
 edge('supports-'+i,'support',i,True,f'exitX={x};exitY=0;entryX=0.5;entryY=1;')
box('boundary','贯穿所有主题的判断边界\n执行能力 ≠ 决策授权  ｜  验证通过 ≠ 全面正确  ｜  验收接受 ≠ 价值实现\n实线：阅读顺序；虚线：平台承载关系。图示为概念模型，不代表能力已经实现。',30,740,1140,110,'#f8fafc',20)
E.ElementTree(f).write(out/'overview.drawio',encoding='utf-8',xml_declaration=True)
