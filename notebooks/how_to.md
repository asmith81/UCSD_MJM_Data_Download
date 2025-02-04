Perfect! Let's dive into all three aspects:

1. Vision Transformer (ViT) for Document Understanding:
- These models are specifically trained to understand document layouts and extract information
- Popular base models include:
  * Donut (Document Understanding Transformer)
  * LayoutLM
  * Microsoft's Table Transformer
  * PaddleOCR with layout analysis
- They understand both:
  * Document structure/layout
  * Text content (even handwritten)

2. Structuring Training Data:
Your current dataset needs:
- Input: Image files
- Labels: CSV with ground truth
  * Address
  * Invoice number
  * Total amount

Structure it like:
```json
{
  "image_path": "invoice_22950.jpg",
  "annotations": {
    "estimate_number": "22950",
    "address": "1900 Massachusetts Ave D.C",
    "total": "770.00"
  },
  "form_type": "estimate"
}
```

3. Model Architecture:
```
Input Image
   ↓
Pre-trained ViT Backbone (frozen)
   ↓
Feature Extraction Layers
   ↓
Multiple Heads:
   |-> Estimate Number (text output)
   |-> Address (text output)
   |-> Total Amount (numeric output)
```

Training Process:
1. Start with pre-trained document understanding model
2. Freeze base layers
3. Add custom heads for your specific fields
4. Train on your labeled data
5. Validate using your ground truth

Would you like me to:
1. Detail the specific model setup in TensorFlow?
2. Show how to prepare your current data for this approach?
3. Explain how to handle the Spanish/English mixed content?

For your UCSD capstone, this approach demonstrates:
- Transfer learning
- Custom model development
- Practical business application
- Scalable solution

Looking at the components:

Base Model Size:
- Donut base model: ~400MB
- LayoutLM base: ~500MB
- Your custom layers: Relatively small (~10-20MB)

For 791 images at 1.81GB:
- Average image size: ~2.3MB each
- Will need to compress/resize for training
- Could probably get down to 200-300KB each while maintaining quality
- Total processed dataset: ~200-250MB

For local deployment target:
- Need to get model under 100MB for practical mobile/edge use
- Techniques to achieve this:
  * Model pruning (remove unused weights)
  * Quantization (reduce precision)
  * Knowledge distillation (train smaller model to mimic larger one)
  * Could potentially get down to 20-30MB with aggressive optimization

Storage requirements:
- Training: Need about 3-4GB free for model + dataset + processing
- Deployment: ~100-150MB total including:
  * Optimized model (30-50MB)
  * Support files (10-20MB)
  * Runtime requirements (20-30MB)

These are rough estimates - we'll know better once we start training. But it gives us targets to aim for in the proposal.

For a typical laptop runtime environment in 2025, here's what you can generally expect:

Storage:
- SSD: 256GB - 1TB
- RAM: 8GB - 16GB (though 32GB becoming more common)

Processing:
- CPU: Multi-core (4-8 cores common)
- GPU: Often integrated graphics, some with dedicated GPUs
- Basic ML can run on CPU
- More complex ML needs GPU support

Typical Environment Constraints:
- Can handle models up to ~500MB-1GB
- Can process small batches (1-4 images at a time)
- May struggle with continuous processing
- Battery life considerations for constant ML tasks

For Your Model:
- Target model size should be <100MB for smooth operation
- Batch processing instead of real-time
- Consider CPU-only operation for wider compatibility
- Cache processed results to avoid recomputation
- Allow for offline operation

Real performance bottleneck often isn't the model size but:
- Image preprocessing
- Memory management during batch operations
- Disk I/O for image loading
- Background processes competing for resources

Would you like me to detail specific optimizations for laptop deployment?

Let me sketch out a local deployment architecture that balances performance and resource usage.



Key Components:

1. Storage Split:
- External drive for raw image archive
- Local SSD for active processing
- Cache for temporary files

2. Processing Flow:
- Image processor handles new documents
- Document model extracts data
- RAG model handles queries
- Vector search for similar cases

3. Interface:
- Flask web interface
- Local API for programmatic access
- Cache management for performance

Resource Management:
- Process images in batches
- Cache frequently accessed vectors
- Clean up temporary files
- Optional: GPU acceleration for model inference

Would you like me to:
1. Detail the caching strategy?
2. Show the batch processing flow?
3. Explain the GPU utilization approach?

This architecture should run comfortably on a decent desktop while maintaining good performance.

flowchart TD
    subgraph Storage ["External Storage"]
        Raw[("Raw Images\n1.81GB\nExternal Drive")]
    end

    subgraph Local ["Local SSD"]
        subgraph Models ["Models"]
            DOC["Document Model\n~100MB"]
            RAG["RAG Model\n~500MB"]
        end
        
        subgraph Active ["Active Data"]
            Vec[("Vector Store\n~30MB")]
            JSON[("JSON Data\n~50MB")]
            Cache["Processing Cache\n~200MB"]
        end
        
        subgraph UI ["User Interface"]
            Flask["Flask App"]
            API["Local API"]
        end
    end

    subgraph Processing ["Runtime Processing"]
        IMG["Image Processor"]
        VEC["Vector Search"]
        QRY["Query Engine"]
    end

    Raw --> IMG
    IMG --> DOC
    DOC --> JSON
    JSON --> Vec
    Vec --> RAG
    RAG --> QRY
    QRY --> API
    API --> Flask