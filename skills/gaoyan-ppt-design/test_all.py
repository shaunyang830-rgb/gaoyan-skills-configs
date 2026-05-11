import sys, os
os.chdir(r'C:\Users\杨顺\Documents\Obsidian Vault')
sys.path.insert(0, '.claude/skills/gaoyan-ppt-design')
from gaoyan_ppt import GaoyanEngine

eng = GaoyanEngine(total_slides=22)

# A. 结构导航
eng.cover('中国餐饮行业\n年度趋势报告', subtitle='Annual Trend Report', date='2026.04', author='高岩科技')
eng.cover_fullscreen('中式餐饮白皮书', subtitle='Chinese Cuisine Whitepaper', date='2026')
eng.toc(items=[(1, '市场总览', 'Market Overview'), (2, '品类分析', 'Category'), (3, '趋势预测', 'Trend')])
eng.section_divider(section_label='PART 01', title='市场总览', subtitle='Market Overview')

# B. 数据统计
eng.big_number('中国餐饮市场规模突破5万亿', number='5.2', unit='万亿元',
               description='同比增长12.3%', detail_items=[('门店数', '800万+'), ('从业人数', '2000万+')],
               tag='总览', sub_conclusion='市场持续回暖', source='Source: 国家统计局')
eng.three_stat('核心增长指标', stats=[
    {'number': '12.3', 'unit': '%', 'label': '同比增长率', 'trend': 'up'},
    {'number': '5.2', 'unit': '万亿', 'label': '市场规模'},
    {'number': '800', 'unit': '万', 'label': '门店总数', 'trend': 'down'},
], tag='总览', source='Source: 高岩餐观')
eng.data_table('Top10品牌门店数', headers=['排名', '品牌', '门店数', '增长率'],
               rows=[['1', '蜜雪冰城', '30000+', '15%'], ['2', '瑞幸咖啡', '18000+', '25%'],
                     ['3', '华莱士', '20000+', '8%'], ['4', '绝味鸭脖', '15000+', '5%']],
               highlight_cols=[2, 3], tag='数据', source='Source: 高岩餐观')

# C. 洞察
eng.key_insight('新茶饮赛道增速放缓但利润提升',
                left_content='新茶饮市场规模达3000亿元，同比增长8.5%。头部品牌加速下沉市场布局。',
                right_takeaways=['头部品牌集中度提升', '下沉市场仍有空间', '供应链成为核心壁垒'],
                tag='洞察', sub_conclusion='品牌化和供应链是关键', source='Source: 高岩')
eng.chart_insight('火锅赛道竞争格局', chart_placeholder_label='火锅品牌竞争力散点图',
                  takeaways=['海底捞品牌力最强', '呷哺呷哺转型效果显著', '区域品牌崛起'],
                  tag='洞察', source='Source: 高岩餐观')

# D. 对比
eng.side_by_side('中式正餐 vs 西式快餐', options=[
    {'heading': '中式正餐', 'points': ['客单价高', '翻台率低', '体验导向']},
    {'heading': '西式快餐', 'points': ['标准化强', '翻台率高', '效率导向']},
], tag='对比', source='Source: 高岩')
eng.before_after('数字化转型效果', before_title='传统模式',
                 before_points=['人工点单', '纸质记账', '经验定价'],
                 after_title='数字化模式', after_points=['扫码点单', '智能收银', 'AI定价'],
                 tag='转型', source='Source: 高岩')
eng.pros_cons('加盟 vs 直营', pros=['扩张速度快', '轻资产运营', '本地化强'],
              cons=['品控难度大', '品牌稀释风险', '管理成本高'], conclusion='建议采用混合模式',
              tag='策略', source='Source: 高岩')

# E. 框架矩阵
eng.matrix_2x2('品牌竞争力评估矩阵', quadrants=[
    {'heading': '明星品牌', 'items': ['海底捞', '太二酸菜鱼']},
    {'heading': '高潜品牌', 'items': ['费大厨', '朱光玉']},
    {'heading': '成熟品牌', 'items': ['肯德基', '麦当劳']},
    {'heading': '挑战品牌', 'items': ['区域小品牌']},
], axis_labels={'top': '高增长', 'bottom': '低增长', 'left': '低市占', 'right': '高市占'},
   tag='矩阵', source='Source: 高岩')
eng.process_chevron('餐饮品牌打造4步法', steps=[
    {'number': 1, 'heading': '市场洞察', 'description': '数据分析+趋势研判'},
    {'number': 2, 'heading': '品牌定位', 'description': '差异化+价值主张'},
    {'number': 3, 'heading': '产品打造', 'description': '菜品研发+供应链'},
    {'number': 4, 'heading': '规模扩张', 'description': '加盟体系+数字化'},
], tag='流程', source='Source: 高岩')
eng.vertical_steps('赋能服务流程', steps=[
    {'number': 1, 'heading': '需求诊断', 'description': '深度调研客户现状'},
    {'number': 2, 'heading': '方案设计', 'description': '定制化数据分析方案'},
    {'number': 3, 'heading': '落地执行', 'description': '数据接入+分析交付'},
    {'number': 4, 'heading': '持续优化', 'description': '月度复盘+迭代升级'},
], tag='服务', source='Source: 高岩')
eng.timeline('高岩科技发展历程', milestones=[
    {'date': '2020', 'heading': '公司成立', 'description': '餐饮数据分析'},
    {'date': '2022', 'heading': '餐观上线', 'description': 'SaaS产品发布'},
    {'date': '2024', 'heading': 'AI赋能', 'description': 'Agent+Skill'},
    {'date': '2026', 'heading': '规模化', 'description': '服务1000+品牌'},
], tag='历程', source='Source: 高岩')

# F. 团队/案例
eng.meet_the_team('核心团队', members=[
    {'name': '杨顺', 'role': '联合创始人', 'description': '数据分析专家'},
    {'name': '张三', 'role': 'CTO', 'description': '技术架构师'},
    {'name': '李四', 'role': 'COO', 'description': '运营管理'},
], tag='团队')
eng.case_study('某连锁火锅品牌数字化案例', sections=[
    {'heading': '背景', 'content': '全国300+门店，运营效率亟需提升'},
    {'heading': '方案', 'content': '接入高岩餐观大数据，定制分析看板'},
    {'heading': '实施', 'content': '3个月完成全链路数据接入'},
], result_box={'heading': '成果', 'content': '运营效率提升35%，翻台率提高12%'},
   tag='案例', source='Source: 高岩')

# G. 图表
eng.grouped_bar('Top品类门店增长对比', categories=['火锅', '奶茶', '咖啡', '快餐'],
                series=['2024', '2025'], data=[[150, 200, 180, 300], [180, 250, 220, 350]],
                tag='数据', source='Source: 高岩餐观')
eng.donut('品类占比', segments=[
    {'label': '火锅', 'value': 35}, {'label': '快餐', 'value': 25},
    {'label': '奶茶', 'value': 20}, {'label': '其他', 'value': 20}],
    center_label='品类占比', summary='火锅仍是第一大品类', tag='数据', source='Source: 高岩')

# H. 高岩特色
eng.egpm_flavor_card('EGPM趋势分析', chart_placeholder_label='EGPM散点图',
                     flavor_cards=[
                         {'title': '麻辣风味', 'description': '川渝地区增长最快', 'image_label': 'Spicy'},
                         {'title': '酸甜风味', 'description': '年轻人最爱', 'image_label': 'Sweet'},
                         {'title': '鲜香风味', 'description': '粤菜系核心', 'image_label': 'Umami'},
                     ], tag='EGPM', source='Source: 高岩餐观')

eng.closing(title='THANKS!', message='数智餐饮 共创味来')

out = eng.save('.claude/skills/gaoyan-ppt-design/test_output.pptx')
print(f'SUCCESS! Generated {out} with {len(eng.prs.slides)} slides')
