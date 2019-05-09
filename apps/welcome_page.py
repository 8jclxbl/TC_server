import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from app import app



welcome_layout = [
    html.Div(id = 'preview',children = [
        html.Div(id = 'w-title-container',children = [
            html.H3('“数智教育”数据可视化创新大赛作品'),
        ],style = {'text-align':'center'}),
        html.Div(id = 'w-team-name', children = [
            html.H5('参赛队伍名称：忽然之间克哈的霓虹为我在闪烁'),
        ],style = {'text-align':'center'}),
        
       
        html.Div(id = 'preview-text',children = [
            
            html.Div(
                children = [
                    html.Hr(),
                    html.P(children = [
                        '本作品基于python的',
                        html.A(id = 'dash-url',children = ['plot.ly'],href = 'https://plot.ly/',target = '_blank'),
                        '的dash框架实现。图表中自带了很多基础的控件，可以对图表进行拖拽选择',
                        '指定区域的大小缩放，具体的特色功能详见提交的控件特色功能文档。',
                        ],className = 'sj-p'
                    ),
                    
                    
                    html.P(children = ["""
                        首先介绍各个主要模块的主要功能。学生域模块中，通过输入学号，显示学生的具体画像，包括了基本信息，成绩，考勤和消费四部分，
                        基本信息模块包含了学生基本信息和任课教师信息(所有仅有表头和一行数据表格并没有使用dash中的表格实现，不支持dash图表的功能，除了这两张表，还有此模块考勤统计的饼图下方的表格)。
                        成绩模块用两张表格分别展示了学生历次考试的总分及排名，历次考试具体课程的分数及排名信息，
                        下方的折线图，展示了学生历次考试的分数趋势，下拉菜单支持选中多门课程进行比较，
                        支持使用原始分数，或是Z值，T值，等第进行比较(Z值，T值，等第的显示可以通过评价指标中的多选下拉菜单进行组合)，并提供了对于下一次考试的等第的预测。
                        考虑到平时成绩和考试成绩的总分差异较大，将平时成绩和考试成绩分开展示。
                        成绩模块之后是考勤模块，采用了一张散点图和表格来统计学生的总体考勤情况，此模块的第二个下拉菜单提供了图和表的切换；
                        可以用此模块第一个下拉菜单选择考勤情况统计，这里用了一张饼图和一张单行表格来显示各学期的出勤情况
                        通过左上角的学期选择下拉菜单，可以选择饼图要展示的学期(学期选项中只有有考勤数据的学期)。
                        消费模块中，我们使用了柱状图和统计表来显示学生的消费情况，其中的第一个下拉菜单，
                        实现了图表的切换，第二个下拉菜单可以选择显示原始数据(总数据)，按年，月，日统计的消费总和的表格或图。
                        另外，对于消费的月数据，我们给出了下月消费的预测，及对学生消费情况的评价。
                    """],className = 'sj-p'),

                    html.P("""
                          课程域分两大模块，班级最高最低分趋势和当前高三的七选三统计。首先，我们提供了根据选定的学期选择具体班级的选项，
                        根据选择结果会给出选中班级所具有的考试数据的各个科目最高分和最低分统计表,下方提供了根据科目显示该班级的给定科目的历次考试最高分最低分趋势图。
                        之后的七选三模块中，我们给出了各个组合选择比例的饼图，单科选择人数的柱状图，根据下拉菜单给定班级的班内选课组合的分布柱状图,
                        根据下拉菜单给出的选课组合在各个班级的分布柱状图。
                    """,className = 'sj-p'),

                    html.P("""
                        群体域数据分析中，首先根据选中的学期和年级，会获取当前学期当前年级的所有的考试的下拉菜单，及选中的考试的科目。
                        根据前面的选择，可以获取选中的年级的某次考试的选中科目(支持总分)的班级平均分及排名，以及选中的年级的选中的科目的各个班级在此次考试中的分数段比较图。
                        下方实现了根据前面选中的学期，年级，考试，获取参与此次考试的选中年级的具体信息的下拉菜单，包括参加此次考试的选中年级的所有班级，本次考试选中年级的考核科目(支持总分)和分数类型。
                        而后，跟据选中的班级，科目，分数类型，获取相应的排名统计表和分数段分布图
                    """,className = 'sj-p'),
                    
                    html.P("""
                        在实现了比赛要求的学生域，课程域和群体域的数据分析之后，额外加入了宿舍域功能。
                        此功能首先筛选出了具有住宿信息的学生所在的班级，根据班级可以选择此班级学生所住的宿舍,然后通过选择宿舍号，可以获取此班级在选中宿舍居住的学生的基本信息。
                        另外加入了同一宿舍学生的消费水平的比较的柱状图。
                    """,className = 'sj-p')
                        ],style = {'margin-left':'5%','margin-right':'5%','padding-bottom':'10%'}
            )
        ])
    ],className = 'text-container'),

    
]