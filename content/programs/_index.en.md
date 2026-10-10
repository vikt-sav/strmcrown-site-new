---
title: "Programs"
description: "My Open Projects and Useful Tools"
lastmod: 2026-10-10
---

This page features a collection of my projects, scripts, and applications.

<div class="resources-grid">

  <div class="resource-card">
    <div class="book-header">
      <h3>Transport Delay Predictor</h3>
      <p class="book-author">Moscow Public Transportation Hackathon • Streaming ML • Geo-matching (HMM)</p>
    </div>
    <p class="book-review">
      Streaming public transit delay prediction: NDTP binary protocol over TCP, GPS matching
      with schedules, HMM mapping of tracks to OSM streets, CatBoost on 69 features with strict anti-leakage.
      Fair streaming evaluation: MAE 42 s vs. 93 s for the baseline. Dispatcher dashboard on MapLibre
      with “what-if” scenarios, Docker Compose (3 services), ONNX export, 18 tests.
      Hackathon solution, built solo in 2 days using agents, then pushed to the repository.
    </p>
    <a href="https://github.com/vikt-sav/transport-delay-predictor" target="_blank" class="resource-link">GitHub →</a>
  </div>

  <div class="resource-card">
    <div class="book-header">
      <h3>Norbert AI</h3>
      <p class="book-author">AI Assistant</p>
    </div>
    <p class="book-review">
      Norbert AI — a ready-to-use architecture for building intelligent assistants. Semantic search, graph, RAG, web search, and scientific database search, annotation, and analytics via LLM.
    </p>
    <a href="https://github.com/vikt-sav/norbert-ai" target="_blank" class="resource-link">GitHub →</a>
  </div>

  <div class="resource-card">
    <div class="book-header">
      <h3>VLM Defect Detection</h3>
      <p class="book-author">Visual Quality Inspection • Qwen2.5-VL • QLoRA fine-tuning</p>
    </div>
    <p class="book-review">
      A device defect inspection pipeline built on a vision-language model: fine-tuning Qwen2.5-VL-3B via QLoRA,
      full cycle from dataset to training, GGUF export, and Ollama inference. Three approaches compared on a
      419-image evaluation set (6 MVTec AD categories): the fine-tuned VLM beats the CV baseline with F1 0.84 vs. 0.75,
      recall 0.93, and 100% valid JSON. Structured output (defect/normal, type, location, severity), 35 tests, FastAPI, CI.
    </p>
    <a href="https://github.com/vikt-sav/vLM-defect-detection" target="_blank" class="resource-link">GitHub →</a>
  </div>

  <div class="resource-card">
    <div class="book-header">
      <h3>Multi-Agent Translation Evaluator</h3>
      <p class="book-author">Translation Quality Evaluation</p>
    </div>
    <p class="book-review">
      A multi-agent system for evaluating the quality of machine translation (English → Russian) using several specialized LLM agents and a moderator. Used for scientific research.
    </p>
    <a href="https://github.com/vikt-sav/multi-agent-translation-evaluator" target="_blank" class="resource-link">GitHub →</a>
  </div>

  <div class="resource-card">
    <div class="book-header">
      <h3>CargaPronto: delivery delay prediction</h3>
      <p class="book-author">Machine learning • clustering + classification • educational project</p>
    </div>
    <p class="book-review">
      K-Means customer segmentation (geography + RFM profiles) and CatBoost delay risk prediction for a logistics operator.
      GroupShuffleSplit by customer, fit-on-train clustering without holdout. Test ROC-AUC 0.7721 (threshold 0.75): clusters contribute +0.015.
      The hypothesis about “problem customers” is only partially confirmed: behavior is informative (15.4% importance), while geography is not (6.0%).
    </p>
    <a href="https://github.com/vikt-sav/unsupervised-learning-prediction-ml" target="_blank" class="resource-link">GitHub →</a>
  </div>

  <div class="resource-card">
    <div class="book-header">
      <h3>Logran</h3>
      <p class="book-author">Running Log</p>
    </div>
    <p class="book-review">
      A simple and convenient app for keeping a running log. Automatic pace and speed calculation, history, progress charts, and support for multiple users.
    </p>
    <a href="https://github.com/vikt-sav/logrun-running-log" target="_blank" class="resource-link">GitHub →</a>
  </div>

  <div class="resource-card">
    <div class="book-header">
      <h3>JPG to PDF Compiler</h3>
      <p class="book-author">Image Converter</p>
    </div>
    <p class="book-review">
      A simple script that automatically collects all numbered JPG files in a folder and combines them into a single PDF document.
    </p>
    <a href="https://github.com/vikt-sav/jpg-to-pdf-compiler" target="_blank" class="resource-link">GitHub →</a>
  </div>

  <div class="resource-card">
    <div class="book-header">
      <h3>Predicting User Age Based on Online Behavior</h3>
      <p class="book-author">Machine Learning • Multiclass Classification</p>
    </div>
    <p class="book-review">
      A learning project to build a model for predicting a user’s age category (0–4) based on internet behavior data. 
      Linear models, feature engineering, metric analysis, and visualization were used.
      Goal: F1-macro ≥ 0.75.
    </p>
    <a href="https://github.com/vikt-sav/user-age-prediction-ml" target="_blank" class="resource-link">GitHub →</a>
  </div>
</div>
