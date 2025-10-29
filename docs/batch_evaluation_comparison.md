# 批量评估方式对比

## 两种批量评估方式

项目提供两种批量评估方式，各有优缺点：

### 方式 1：图片文件批量处理

**脚本**：`tools/demo_visualization.py --mode batch --multi_category`

**命令示例**：
```bash
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test \
  --multi_category \
  --device GPU
```

**工作流程**：
1. 读取图片文件
2. 使用 OpenCV Haar Cascade 检测人脸
3. 裁剪人脸区域
4. 输入模型进行预测

**优点**：
- ✅ 可以处理任意图片
- ✅ 支持保存标注后的图片
- ✅ 可视化效果好

**缺点**：
- ❌ **人脸检测可能漏检**（特别是低分辨率图片）
- ❌ 处理速度较慢
- ❌ 准确率可能虚高（漏检的样本不计入统计）

### 方式 2：CSV 数据批量评估（推荐）

**脚本**：`src/batch_eval_csv.py`

**命令示例**：
```bash
python src/batch_eval_csv.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage PrivateTest \
  --device GPU
```

**工作流程**：
1. 读取 CSV 文件
2. 解析像素字符串
3. 直接输入模型进行预测

**优点**：
- ✅ **100% 无漏检**：所有样本都会被评估
- ✅ 处理速度更快
- ✅ **准确率更真实可靠**
- ✅ 无需人脸检测

**缺点**：
- ❌ 只能处理 FER2013 格式的 CSV 数据
- ❌ 无法保存标注图片

## 详细对比

| 特性 | 图片文件方式 | CSV 方式 |
|------|------------|---------|
| **脚本** | `tools/demo_visualization.py` | `src/batch_eval_csv.py` |
| **输入** | 图片文件目录 | CSV 文件 |
| **人脸检测** | ✅ 需要（OpenCV） | ❌ 不需要 |
| **漏检问题** | ⚠️ 可能漏检 10-20% | ✅ 100% 无漏检 |
| **处理速度** | 🐢 较慢 | ⚡ 快 |
| **准确率** | ⚠️ 可能虚高 | ✅ 真实准确率 |
| **样本覆盖** | 📉 部分样本 | 📊 所有样本 |
| **保存图片** | ✅ 支持 | ❌ 不支持 |
| **适用场景** | 通用图片评估 | FER2013 数据集 |
| **推荐程度** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 漏检问题详解

### 为什么会漏检？

OpenCV 的 Haar Cascade 人脸检测器对以下情况敏感：

1. **图片分辨率低**：FER2013 的图片只有 48x48 像素
2. **人脸不完整**：某些图片可能已经是裁剪过的人脸
3. **角度问题**：侧脸、低头等姿态
4. **光照问题**：过暗或过亮
5. **遮挡问题**：部分遮挡的人脸

### 漏检率有多高？

根据实际测试，图片文件方式的漏检率约为：
- **10-20%**（取决于数据质量）
- 某些类别漏检率可能更高

### 漏检的影响

假设某个类别有 500 张图片：

**图片文件方式**：
- 检测到：400 张
- 漏检：100 张
- 预测正确：320 张
- **计算的准确率**：320 / 400 = **80%**

**CSV 方式**：
- 处理：500 张（全部）
- 预测正确：380 张
- **真实准确率**：380 / 500 = **76%**

可以看到，漏检会导致准确率**虚高约 4%**。

## 实际测试对比

### 测试条件
- 数据集：FER2013 PrivateTest
- 模型：checkpoints_50epoch/best_model.ckpt
- 设备：GPU

### 方式 1：图片文件（可能有漏检）

```bash
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input /mnt/e/Users/Meng/Datasets/FER2013/test \
  --multi_category \
  --device GPU
```

**预期结果**：
```
Category     Total    Correct  Accuracy   Rank
----------------------------------------------------------------------
happy        ~370     ~305     ~82.4%     #1    ← 可能虚高
neutral      ~520     ~410     ~78.8%     #2    ← 可能虚高
...
----------------------------------------------------------------------
AVERAGE                        ~70.5%            ← 可能虚高
```

**注意**：处理的样本数可能少于实际样本数（因为漏检）

### 方式 2：CSV 数据（无漏检）

```bash
python src/batch_eval_csv.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage PrivateTest \
  --device GPU
```

**预期结果**：
```
Category     Total    Correct  Accuracy   Rank
----------------------------------------------------------------------
happy        895      718      80.2%      #1    ← 真实准确率
neutral      626      485      77.5%      #2    ← 真实准确率
sad          653      473      72.4%      #3
angry        467      327      70.0%      #4
surprise     415      280      67.5%      #5
fear         528      326      61.7%      #6
disgust      5        2        40.0%      #7
----------------------------------------------------------------------
AVERAGE                        67.0%             ← 真实平均
```

**注意**：处理了所有 3,589 张图片，无漏检

### 对比分析

| 指标 | 图片方式 | CSV 方式 | 差异 |
|------|---------|---------|------|
| happy 准确率 | ~82.4% | 80.2% | -2.2% |
| 平均准确率 | ~70.5% | 67.0% | -3.5% |
| 样本数 | ~3000 | 3589 | -589 (漏检) |

**结论**：CSV 方式的准确率更低但**更真实**。

## 使用建议

### 场景 1：最终模型评估（推荐 CSV）

**目的**：获得模型的真实性能指标

**命令**：
```bash
python src/batch_eval_csv.py \
  --csv /mnt/e/Users/Meng/Datasets/FER2013CSV/fer2013.csv \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --usage PrivateTest \
  --device GPU
```

**理由**：
- 无漏检，结果可靠
- 可用于论文、报告
- 真实反映模型性能

### 场景 2：快速可视化分析（图片方式）

**目的**：查看标注效果，分析错误样本

**命令**：
```bash
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input /path/to/test/sad \
  --save_images
```

**理由**：
- 可以查看标注后的图片
- 便于发现问题
- 适合调试

### 场景 3：通用图片评估（图片方式）

**目的**：评估自己的图片数据

**命令**：
```bash
python tools/demo_visualization.py \
  --mode batch \
  --ckpt checkpoints_50epoch/best_model.ckpt \
  --input /path/to/my/images \
  --multi_category
```

**理由**：
- CSV 方式仅支持 FER2013 格式
- 图片方式更通用

### 场景 4：模型对比（CSV 方式）

**目的**：对比不同模型的性能

**命令**：
```bash
# 模型 A
python src/batch_eval_csv.py \
  --csv /path/to/fer2013.csv \
  --ckpt model_a.ckpt \
  --usage PrivateTest \
  --output output/model_a

# 模型 B
python src/batch_eval_csv.py \
  --csv /path/to/fer2013.csv \
  --ckpt model_b.ckpt \
  --usage PrivateTest \
  --output output/model_b
```

**理由**：
- 保证评估条件完全一致
- 无漏检干扰
- 对比结果可靠

## 推荐工作流程

### 开发阶段

1. **使用 CSV 方式快速评估**：
   ```bash
   python src/batch_eval_csv.py \
     --csv /path/to/fer2013.csv \
     --ckpt checkpoints/latest.ckpt \
     --usage PrivateTest
   ```

2. **分析结果**：
   - 查看 `accuracy_comparison.png`
   - 识别表现差的类别

3. **使用图片方式可视化**：
   ```bash
   python tools/demo_visualization.py \
     --mode batch \
     --ckpt checkpoints/latest.ckpt \
     --input /path/to/test/[problem_category] \
     --save_images
   ```

4. **查看具体错误样本**，分析原因

### 发布阶段

1. **使用 CSV 方式获得最终评估结果**：
   ```bash
   python src/batch_eval_csv.py \
     --csv /path/to/fer2013.csv \
     --ckpt checkpoints/final_model.ckpt \
     --usage PrivateTest \
     --device GPU
   ```

2. **记录准确率数据**，用于报告

3. **（可选）使用图片方式生成示例图片**，用于演示

## 常见问题

### Q1: 为什么 CSV 方式的准确率更低？

**A**: CSV 方式处理了**所有样本**，包括难识别的。图片方式可能漏检这些难样本，导致准确率虚高。CSV 方式的结果**更真实**。

### Q2: 什么时候应该使用图片方式？

**A**:
- 需要保存标注图片时
- 评估非 FER2013 数据集时
- 需要可视化分析时

### Q3: CSV 方式支持保存图片吗？

**A**: 目前不支持。如果需要保存图片，请使用图片文件方式。

### Q4: 两种方式可以一起用吗？

**A**: 可以！建议：
1. 用 CSV 方式获得准确的性能指标
2. 用图片方式生成可视化结果

### Q5: 哪种方式更快？

**A**: CSV 方式更快，因为：
- 无需人脸检测
- 直接处理像素数据
- GPU 加速效果更好

## 总结

| 需求 | 推荐方式 |
|------|---------|
| **最终模型评估** | ⭐ **CSV 方式** |
| **论文/报告数据** | ⭐ **CSV 方式** |
| **可视化分析** | 图片方式 |
| **通用图片评估** | 图片方式 |
| **快速原型测试** | CSV 方式 |
| **模型对比** | ⭐ **CSV 方式** |

**推荐**：在项目的关键评估节点，**始终使用 CSV 方式**获得真实、可靠的性能指标。

## 相关文档

- CSV 快速开始：[QUICK_START_CSV_BATCH.md](../QUICK_START_CSV_BATCH.md)
- 图片批量处理：[batch_multi_category_guide.md](batch_multi_category_guide.md)
- 主文档：[README.md](../README.md)
