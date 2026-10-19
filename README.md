# Lab: Vision-Language Models (CLIP & LLaVA)

PhD lab on vision-language models with PyTorch and Hugging Face Transformers.

## Files
| Path | Description |
|---|---|
| `LAB_CLIP_LLaVA.ipynb` | Notebook with code, outputs and answers (Q1 to Q36) |
| `image.jpg` | Main test image (Exercises 2, 3, 4, 6, 13) |
| `eval_images/` | Labeled images for the CLIP evaluation (Exercise 5) |
| `images/` | Image database for retrieval (Exercises 7, 8) |
| `vqa_images/` | Images for LLaVA VQA and the hallucination test (Exercises 10 to 12) |
| `download_images.py` | Script used to download the images from Wikimedia Commons |
| `CREDITS.md` | Source and license of each image |
| `screenshots/` | Screenshots of the Gradio interface (mini-project) |

## Results
| Experiment | Result |
|---|---|
| CLIP zero-shot classification (12 images, 6 classes) | 100% accuracy |
| CLIP retrieval, "a person playing football" (24 images) | 4/5 relevant in the top 5 |
| LLaVA-1.5-7B VQA (5 images x 5 questions) | 72% (18/25) |
| Hallucination test (no bicycle in the image) | LLaVA describes a black bicycle |
| Mini-project | Image assistant with CLIP + LLaVA and a Gradio interface |

## How to run
Open `LAB_CLIP_LLaVA.ipynb` in Google Colab with a GPU runtime (T4) and run the cells in order.
