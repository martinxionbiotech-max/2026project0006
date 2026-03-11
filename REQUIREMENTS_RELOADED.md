# Dating Reality Calculator – Reloaded Requirements (重新拉取需求)

## 1. 产品目标
构建一个可传播、可解释、移动端友好的 Dating Reality Calculator，输出完整报告：
- Dating Pool（匹配池）
- Dating Market Value（价值评分）
- Competition Ratio（竞争比）
- Future Dating Probability（未来概率）

## 2. 核心模块
1. **Dating Pool Calculator**
   - 输入：目标性别、年龄区间、身高下限、收入下限（USD）、婚姻状态、BMI分类、国家
   - 逻辑：`P(age) * P(height) * P(income) * P(marital) * P(bmi)`
   - 输出：匹配比例、匹配人口、总目标人口

2. **Dating Market Value Calculator**
   - 输入：年龄、身高、收入、fitness、face、education、confidence、social skills
   - 逻辑：`physical(50%) + status(30%) + personality(20%)`
   - 输出：score、percentile、category

3. **Competition Ratio Calculator**
   - 逻辑：`eligible_men = male_population * target_male_percentage`
   - 输出：`1 man : X women`

4. **Reality Adjustment Simulator**
   - 作用：实时展示身高/收入/年龄上限变化对匹配池规模的影响，帮助用户理解“标准微调 -> 匹配数量显著变化”。

5. **Future Dating Probability**
   - 逻辑：复利式概率到 40 岁的累计遇见概率
   - 输出：`Chance by 40`

## 3. 国家与数据要求
必须支持国家：
- USA
- Canada
- United Kingdom
- Australia

每个国家至少包含：
- 总人口、男女人口
- 年龄分布（18-24 / 25-35 / 36-45）
- 身高分布（>=175/180/185）
- 收入分布（>=50k/100k/150k，单位仍用 USD）
- 婚姻状态分布（single/married/divorced）
- BMI分布（non-obese/overweight/obese）
- marriage_rate

## 4. 文案与页面结构要求
- 首页标题下方使用 **最多 2 句话** 的 introduction。
- 不在 introduction 中放页面跳转链接。
- introduction 需自然覆盖以下关键词语义（非堆砌）：
  - Male Delusion Calculator
  - Female Delusion Calculator
  - Dating Pool Calculator
  - Dating Market Value Calculator
  - Dating Reality Calculator

## 5. 交互与体验要求
- Generate 按钮需要明确点击反馈（文字状态/视觉状态）。
- 保持移动端可用性：
  - 小屏单列布局
  - 按钮可点面积足够
  - 表单在手机端可读可操作

## 6. 表单字段策略
- `Marital Status` 与 `BMI` 不应只有单一固定值。
- 若保留下拉，应提供有效多选项并影响计算结果。

## 7. SEO 与结构化数据
- 保留基础 SEO：title/description/canonical/robots
- 保留结构化数据：WebApplication + FAQPage
- 保留基础爬虫资产：`robots.txt` + `sitemap.xml`

## 8. 验收标准（DoD）
- 以上 5 个模块可运行且能生成报告。
- 4 个国家数据在 UI 可切换且结果变化。
- Marital/BMI 选择会改变 Dating Pool 输出。
- Generate 有点击反馈。
- 移动端截图验证通过。
- 基础检查通过：`node --check`、JSON 解析校验。


## 9. 再次拉取请求（V2）
- 本次为“再次发起拉取请求”，用于确认当前需求基线继续生效，并作为后续迭代唯一对齐文档。
- 当前确认项：
  1. 首页 introduction 维持 2 句话、无链接。
  2. 国家维持 USA / Canada / UK / Australia，收入口径统一按 USD。
  3. Reality Adjustment Simulator 需保留作用说明并可观察参数变化影响。
  4. Marital Status 与 BMI 必须为有效可选项，且结果受其影响。
  5. Generate 按钮必须有点击反馈（文案或视觉态）。
- 若后续新增需求，以本节为基准递增版本（V3、V4...）。

## 10. 本轮执行输出
- 输出物：更新后的 `REQUIREMENTS_RELOADED.md`（含 V2 再次拉取说明）。
- 目的：避免需求漂移，确保开发与验收基准一致。


## 11. 拉取创建记录（V3）
- 本次按“创建拉取”请求执行，在新部署分支上创建可追踪提交并发起 PR。
- 目的：确保本轮进入可审阅状态，便于后续继续基于同一需求基线迭代。
- 分支建议：`deploy/new-branch`（当前执行分支）。
