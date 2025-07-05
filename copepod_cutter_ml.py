#!/usr/bin/env python3
"""
🦐 Recortador de Copépodos con Machine Learning
Extracción automática de formas usando múltiples técnicas de ML
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
import os
import requests
from typing import Tuple, List, Optional
import json

class CopepodImageCutterML:
    def __init__(self, image_path: str):
        """
        Inicializar recortador con imagen de copépodo
        
        Args:
            image_path: Ruta a la imagen del copépodo
        """
        self.image_path = image_path
        self.original_image = None
        self.processed_results = {}
        
        # Cargar imagen
        self.load_image()
        
        print(f"🦐 Recortador ML inicializado con: {image_path}")
    
    def load_image(self):
        """Cargar y preparar imagen"""
        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f"❌ Imagen no encontrada: {self.image_path}")
        
        # Cargar con OpenCV
        self.original_image = cv2.imread(self.image_path)
        self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        
        print(f"✅ Imagen cargada: {self.original_image.shape}")
    
    def segment_by_color(self, tolerance: int = 25) -> np.ndarray:
        """
        Segmentación por color usando análisis HSV
        
        Args:
            tolerance: Tolerancia de color para segmentación
            
        Returns:
            Máscara binaria del copépodo
        """
        print("🎯 Iniciando segmentación por color...")
        
        # Convertir a HSV para mejor separación de colores
        hsv = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2HSV)
        
        # Detectar color de fondo analizando esquinas
        corners = [
            hsv[0, 0],  # Superior izquierda
            hsv[0, -1],  # Superior derecha
            hsv[-1, 0],  # Inferior izquierda
            hsv[-1, -1]  # Inferior derecha
        ]
        
        # Promedio de colores de fondo
        bg_color = np.mean(corners, axis=0).astype(np.uint8)
        
        # Crear máscara para el fondo
        lower_bg = np.array([max(0, bg_color[0] - tolerance), 50, 50])
        upper_bg = np.array([min(179, bg_color[0] + tolerance), 255, 255])
        
        # Máscara del fondo
        bg_mask = cv2.inRange(hsv, lower_bg, upper_bg)
        
        # Máscara del copépodo (inversa del fondo)
        copepod_mask = cv2.bitwise_not(bg_mask)
        
        # Operaciones morfológicas para limpiar
        kernel = np.ones((3, 3), np.uint8)
        copepod_mask = cv2.morphologyEx(copepod_mask, cv2.MORPH_CLOSE, kernel)
        copepod_mask = cv2.morphologyEx(copepod_mask, cv2.MORPH_OPEN, kernel)
        
        # Encontrar contorno más grande
        contours, _ = cv2.findContours(copepod_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Seleccionar contorno más grande
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Crear máscara limpia
            clean_mask = np.zeros_like(copepod_mask)
            cv2.fillPoly(clean_mask, [largest_contour], 255)
            
            copepod_mask = clean_mask
        
        self.processed_results['color_segmentation'] = copepod_mask
        print("✅ Segmentación por color completada")
        
        return copepod_mask
    
    def edge_detection_canny(self, low_threshold: int = 50, high_threshold: int = 150) -> np.ndarray:
        """
        Detección de bordes usando algoritmo Canny
        
        Args:
            low_threshold: Umbral bajo para Canny
            high_threshold: Umbral alto para Canny
            
        Returns:
            Máscara basada en detección de bordes
        """
        print("🔍 Iniciando detección de bordes...")
        
        # Convertir a escala de grises
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
        
        # Aplicar filtro Gaussiano para reducir ruido
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Detección de bordes Canny
        edges = cv2.Canny(blurred, low_threshold, high_threshold)
        
        # Dilatar bordes para conectar fragmentos
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Crear máscara del contorno más grande
        mask = np.zeros_like(gray)
        
        if contours:
            # Filtrar contornos por área
            min_area = gray.shape[0] * gray.shape[1] * 0.01  # Al menos 1% de la imagen
            valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
            
            if valid_contours:
                largest_contour = max(valid_contours, key=cv2.contourArea)
                cv2.fillPoly(mask, [largest_contour], 255)
        
        self.processed_results['edge_detection'] = mask
        print("✅ Detección de bordes completada")
        
        return mask
    
    def ai_background_removal_advanced(self, confidence: float = 0.8) -> np.ndarray:
        """
        Remoción de fondo usando técnicas avanzadas de ML
        
        Args:
            confidence: Nivel de confianza para la segmentación
            
        Returns:
            Máscara refinada usando ML
        """
        print("🧠 Iniciando remoción IA avanzada...")
        
        # Análisis de características específicas de copépodos
        features = self._extract_copepod_features()
        
        # Segmentación usando K-means clustering
        kmeans_mask = self._kmeans_segmentation(n_clusters=4)
        
        # Análisis de transparencia y morfología
        transparency_mask = self._analyze_transparency()
        
        # Detección de características anatómicas
        anatomy_mask = self._detect_copepod_anatomy()
        
        # Combinar todas las máscaras con pesos
        combined_mask = (
            kmeans_mask * 0.4 +
            transparency_mask * 0.3 +
            anatomy_mask * 0.3
        )
        
        # Normalizar y aplicar umbral de confianza
        combined_mask = (combined_mask > confidence * 255).astype(np.uint8) * 255
        
        # Refinamiento morfológico
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
        
        self.processed_results['ai_advanced'] = combined_mask
        print("✅ Remoción IA avanzada completada")
        
        return combined_mask
    
    def _extract_copepod_features(self) -> dict:
        """Extraer características específicas de copépodos"""
        features = {}
        
        # Convertir a diferentes espacios de color
        hsv = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2HSV)
        lab = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2LAB)
        
        # Detectar regiones naranjas/rojas típicas de copépodos
        orange_lower = np.array([5, 100, 100])
        orange_upper = np.array([25, 255, 255])
        orange_mask = cv2.inRange(hsv, orange_lower, orange_upper)
        
        # Detectar regiones semi-transparentes
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
        transparency_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
        
        # Detectar puntos oscuros (ojos)
        dark_mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)[1]
        
        features.update({
            'orange_regions': orange_mask,
            'transparency': transparency_mask,
            'dark_spots': dark_mask
        })\n        \n        return features\n    \n    def _kmeans_segmentation(self, n_clusters: int = 4) -> np.ndarray:\n        \"\"\"Segmentación usando K-means clustering\"\"\"\n        # Reshape imagen para K-means\n        data = self.original_image.reshape((-1, 3))\n        data = np.float32(data)\n        \n        # Aplicar K-means\n        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)\n        _, labels, centers = cv2.kmeans(data, n_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)\n        \n        # Reshape resultados\n        centers = np.uint8(centers)\n        segmented = centers[labels.flatten()]\n        segmented = segmented.reshape(self.original_image.shape)\n        \n        # Identificar cluster del copépodo (usualmente el más colorido)\n        cluster_scores = []\n        for i in range(n_clusters):\n            cluster_mask = (labels.flatten() == i).reshape(self.original_image.shape[:2])\n            cluster_color = centers[i]\n            \n            # Score basado en diferencia de color con esquinas (fondo)\n            corner_color = np.mean([\n                self.original_image[0, 0],\n                self.original_image[0, -1],\n                self.original_image[-1, 0],\n                self.original_image[-1, -1]\n            ], axis=0)\n            \n            color_diff = np.linalg.norm(cluster_color - corner_color)\n            area_ratio = np.sum(cluster_mask) / cluster_mask.size\n            \n            # Copépodos suelen tener diferencia de color alta y área moderada\n            score = color_diff * (1 - abs(area_ratio - 0.25))\n            cluster_scores.append(score)\n        \n        # Seleccionar mejor cluster\n        best_cluster = np.argmax(cluster_scores)\n        copepod_mask = (labels.flatten() == best_cluster).reshape(self.original_image.shape[:2])\n        \n        return (copepod_mask * 255).astype(np.uint8)\n    \n    def _analyze_transparency(self) -> np.ndarray:\n        \"\"\"Analizar regiones de transparencia típicas de copépodos\"\"\"\n        # Convertir a escala de grises\n        gray = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)\n        \n        # Detectar regiones claras pero no completamente blancas\n        # (copépodos son semi-transparentes)\n        lower_thresh = 180\n        upper_thresh = 245\n        \n        transparency_mask = cv2.inRange(gray, lower_thresh, upper_thresh)\n        \n        # Dilatar ligeramente para capturar bordes\n        kernel = np.ones((3, 3), np.uint8)\n        transparency_mask = cv2.dilate(transparency_mask, kernel, iterations=1)\n        \n        return transparency_mask\n    \n    def _detect_copepod_anatomy(self) -> np.ndarray:\n        \"\"\"Detectar características anatómicas específicas de copépodos\"\"\"\n        gray = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)\n        height, width = gray.shape\n        \n        # Máscara combinada de anatomía\n        anatomy_mask = np.zeros_like(gray)\n        \n        # 1. Detectar cuerpo principal (región central más grande)\n        # Aplicar threshold adaptativo\n        adaptive_thresh = cv2.adaptiveThreshold(\n            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2\n        )\n        \n        # Invertir (copépodo será blanco)\n        body_mask = cv2.bitwise_not(adaptive_thresh)\n        \n        # 2. Detectar antenas (líneas delgadas desde la cabeza)\n        # Usar detector de líneas\n        edges = cv2.Canny(gray, 50, 150)\n        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=30, minLineLength=20, maxLineGap=10)\n        \n        line_mask = np.zeros_like(gray)\n        if lines is not None:\n            for line in lines:\n                x1, y1, x2, y2 = line[0]\n                cv2.line(line_mask, (x1, y1), (x2, y2), 255, 2)\n        \n        # 3. Detectar puntos de interés (ojos, estructuras internas)\n        # Usar detector de blobs\n        blob_mask = np.zeros_like(gray)\n        \n        # Detectar regiones circulares pequeñas y oscuras\n        circles = cv2.HoughCircles(\n            gray, cv2.HOUGH_GRADIENT, 1, 20,\n            param1=50, param2=30, minRadius=2, maxRadius=10\n        )\n        \n        if circles is not None:\n            circles = np.round(circles[0, :]).astype(\"int\")\n            for (x, y, r) in circles:\n                cv2.circle(blob_mask, (x, y), r, 255, -1)\n        \n        # Combinar todas las características anatómicas\n        anatomy_mask = cv2.bitwise_or(body_mask, line_mask)\n        anatomy_mask = cv2.bitwise_or(anatomy_mask, blob_mask)\n        \n        # Operaciones morfológicas para conectar estructuras\n        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))\n        anatomy_mask = cv2.morphologyEx(anatomy_mask, cv2.MORPH_CLOSE, kernel)\n        \n        return anatomy_mask\n    \n    def hybrid_processing(self, \n                         color_weight: float = 0.4,\n                         edge_weight: float = 0.3,\n                         ai_weight: float = 0.3) -> np.ndarray:\n        \"\"\"Procesamiento híbrido combinando todas las técnicas\"\"\"\n        print(\"⚡ Iniciando procesamiento híbrido...\")\n        \n        # Ejecutar todas las técnicas\n        color_mask = self.segment_by_color()\n        edge_mask = self.edge_detection_canny()\n        ai_mask = self.ai_background_removal_advanced()\n        \n        # Normalizar máscaras\n        color_mask = color_mask.astype(np.float32) / 255.0\n        edge_mask = edge_mask.astype(np.float32) / 255.0\n        ai_mask = ai_mask.astype(np.float32) / 255.0\n        \n        # Combinar con pesos\n        total_weight = color_weight + edge_weight + ai_weight\n        combined_mask = (\n            color_mask * color_weight +\n            edge_mask * edge_weight +\n            ai_mask * ai_weight\n        ) / total_weight\n        \n        # Aplicar umbral y convertir a máscara binaria\n        threshold = 0.5\n        final_mask = (combined_mask > threshold).astype(np.uint8) * 255\n        \n        # Refinamiento final\n        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))\n        final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel)\n        final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)\n        \n        self.processed_results['hybrid'] = final_mask\n        print(\"✅ Procesamiento híbrido completado\")\n        \n        return final_mask\n    \n    def apply_mask_to_image(self, mask: np.ndarray) -> np.ndarray:\n        \"\"\"Aplicar máscara a imagen original para extraer copépodo\"\"\"\n        # Crear imagen RGBA\n        result = np.zeros((self.original_image.shape[0], self.original_image.shape[1], 4), dtype=np.uint8)\n        \n        # Copiar canales RGB\n        result[:, :, :3] = self.original_image\n        \n        # Usar máscara como canal alpha\n        result[:, :, 3] = mask\n        \n        return result\n    \n    def save_result(self, result_image: np.ndarray, output_path: str):\n        \"\"\"Guardar imagen resultado\"\"\"\n        # Convertir a PIL Image para guardar con transparencia\n        pil_image = Image.fromarray(result_image, 'RGBA')\n        pil_image.save(output_path, 'PNG')\n        print(f\"💾 Resultado guardado: {output_path}\")\n    \n    def visualize_results(self):\n        \"\"\"Visualizar todos los resultados\"\"\"\n        fig, axes = plt.subplots(2, 3, figsize=(15, 10))\n        \n        # Imagen original\n        axes[0, 0].imshow(self.original_image)\n        axes[0, 0].set_title('🦐 Original')\n        axes[0, 0].axis('off')\n        \n        # Resultados de técnicas individuales\n        techniques = [\n            ('color_segmentation', '🎯 Segmentación Color'),\n            ('edge_detection', '🔍 Edge Detection'),\n            ('ai_advanced', '🧠 IA Avanzada'),\n            ('hybrid', '⚡ Híbrido ML')\n        ]\n        \n        positions = [(0, 1), (0, 2), (1, 0), (1, 1)]\n        \n        for (technique, title), (row, col) in zip(techniques, positions):\n            if technique in self.processed_results:\n                mask = self.processed_results[technique]\n                result = self.apply_mask_to_image(mask)\n                axes[row, col].imshow(result)\n                axes[row, col].set_title(title)\n            else:\n                axes[row, col].text(0.5, 0.5, 'No procesado', \n                                  ha='center', va='center', transform=axes[row, col].transAxes)\n            axes[row, col].axis('off')\n        \n        # Mejor resultado final\n        if 'hybrid' in self.processed_results:\n            best_mask = self.processed_results['hybrid']\n            best_result = self.apply_mask_to_image(best_mask)\n            axes[1, 2].imshow(best_result)\n            axes[1, 2].set_title('🏆 Mejor Resultado')\n        else:\n            axes[1, 2].text(0.5, 0.5, 'Ejecutar híbrido', \n                          ha='center', va='center', transform=axes[1, 2].transAxes)\n        axes[1, 2].axis('off')\n        \n        plt.tight_layout()\n        plt.show()\n    \n    def calculate_accuracy_metrics(self, mask: np.ndarray) -> dict:\n        \"\"\"Calcular métricas de precisión\"\"\"\n        total_pixels = mask.size\n        foreground_pixels = np.sum(mask > 0)\n        \n        # Ratio de píxeles de primer plano\n        foreground_ratio = foreground_pixels / total_pixels\n        \n        # Análisis de forma (copépodos son típicamente alargados)\n        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)\n        \n        shape_metrics = {}\n        if contours:\n            largest_contour = max(contours, key=cv2.contourArea)\n            \n            # Calcular aspect ratio\n            rect = cv2.minAreaRect(largest_contour)\n            width, height = rect[1]\n            aspect_ratio = max(width, height) / min(width, height) if min(width, height) > 0 else 0\n            \n            # Calcular solidez (área/área del hull convexo)\n            area = cv2.contourArea(largest_contour)\n            hull = cv2.convexHull(largest_contour)\n            hull_area = cv2.contourArea(hull)\n            solidity = area / hull_area if hull_area > 0 else 0\n            \n            shape_metrics = {\n                'aspect_ratio': aspect_ratio,\n                'solidity': solidity,\n                'area': area\n            }\n        \n        # Estimación de precisión basada en heurísticas\n        # Copépodos típicamente ocupan 15-40% de la imagen\n        expected_ratio = 0.25\n        ratio_score = max(0, 100 - abs(foreground_ratio - expected_ratio) * 200)\n        \n        # Copépodos suelen tener aspect ratio entre 2-5\n        aspect_score = 100\n        if 'aspect_ratio' in shape_metrics:\n            expected_aspect = 3.0\n            aspect_score = max(0, 100 - abs(shape_metrics['aspect_ratio'] - expected_aspect) * 20)\n        \n        # Score combinado\n        overall_accuracy = (ratio_score + aspect_score) / 2\n        \n        return {\n            'foreground_ratio': foreground_ratio,\n            'ratio_score': ratio_score,\n            'aspect_score': aspect_score,\n            'overall_accuracy': overall_accuracy,\n            'shape_metrics': shape_metrics\n        }\n    \n    def process_all_techniques(self, output_dir: str = \"results\"):\n        \"\"\"Procesar con todas las técnicas y guardar resultados\"\"\"\n        os.makedirs(output_dir, exist_ok=True)\n        \n        print(\"🦐 Procesando con todas las técnicas ML...\")\n        \n        # Técnica 1: Segmentación por color\n        color_mask = self.segment_by_color()\n        color_result = self.apply_mask_to_image(color_mask)\n        self.save_result(color_result, os.path.join(output_dir, \"copepod_color_segmentation.png\"))\n        \n        # Técnica 2: Edge detection\n        edge_mask = self.edge_detection_canny()\n        edge_result = self.apply_mask_to_image(edge_mask)\n        self.save_result(edge_result, os.path.join(output_dir, \"copepod_edge_detection.png\"))\n        \n        # Técnica 3: IA avanzada\n        ai_mask = self.ai_background_removal_advanced()\n        ai_result = self.apply_mask_to_image(ai_mask)\n        self.save_result(ai_result, os.path.join(output_dir, \"copepod_ai_advanced.png\"))\n        \n        # Técnica 4: Híbrido\n        hybrid_mask = self.hybrid_processing()\n        hybrid_result = self.apply_mask_to_image(hybrid_mask)\n        self.save_result(hybrid_result, os.path.join(output_dir, \"copepod_hybrid_ml.png\"))\n        \n        # Calcular métricas para cada técnica\n        print(\"\\n📊 Métricas de Precisión:\")\n        techniques = {\n            'Color': color_mask,\n            'Edge': edge_mask,\n            'IA': ai_mask,\n            'Híbrido': hybrid_mask\n        }\n        \n        for name, mask in techniques.items():\n            metrics = self.calculate_accuracy_metrics(mask)\n            print(f\"{name}: {metrics['overall_accuracy']:.1f}% precisión\")\n        \n        print(f\"\\n✅ Todos los resultados guardados en: {output_dir}\")\n        \n        return {\n            'color': color_result,\n            'edge': edge_result,\n            'ai': ai_result,\n            'hybrid': hybrid_result\n        }\n\n\ndef main():\n    \"\"\"Función principal para probar el recortador\"\"\"\n    # Ruta a la imagen de prueba\n    image_path = \"copepodo_image.png\"\n    \n    if not os.path.exists(image_path):\n        print(f\"❌ Imagen no encontrada: {image_path}\")\n        print(\"📁 Asegúrate de que la imagen esté en el directorio actual\")\n        return\n    \n    try:\n        # Crear instancia del recortador\n        cutter = CopepodImageCutterML(image_path)\n        \n        # Procesar con todas las técnicas\n        results = cutter.process_all_techniques()\n        \n        # Visualizar resultados\n        cutter.visualize_results()\n        \n        print(\"\\n🦐 Procesamiento completado exitosamente!\")\n        print(\"💡 Los archivos PNG resultantes pueden usarse directamente en el simulador oceánico\")\n        \n    except Exception as e:\n        print(f\"❌ Error durante el procesamiento: {e}\")\n        import traceback\n        traceback.print_exc()\n\n\nif __name__ == \"__main__\":\n    main()