// Fix para el procesamiento híbrido ML
// Agregar esta función a la clase CopepodImageCutterML

hybridCombination(colorMask, edgeMask, aiMask, weightColor, weightEdge, weightAI) {
    console.log('🔧 Iniciando combinación híbrida manual...');
    
    // Determinar la máscara de referencia (la primera disponible)
    let referenceMask = colorMask || edgeMask || aiMask;
    if (!referenceMask) {
        throw new Error('No hay máscaras disponibles para combinar');
    }
    
    const maskLength = referenceMask.length;
    const combined = new Array(maskLength).fill(0);
    
    // Normalizar pesos
    const totalWeight = weightColor + weightEdge + weightAI;
    if (totalWeight === 0) {
        throw new Error('La suma de pesos no puede ser cero');
    }
    
    const normWeightColor = weightColor / totalWeight;
    const normWeightEdge = weightEdge / totalWeight;
    const normWeightAI = weightAI / totalWeight;
    
    console.log('📊 Pesos normalizados:', {
        color: normWeightColor.toFixed(2),
        edge: normWeightEdge.toFixed(2), 
        ai: normWeightAI.toFixed(2)
    });
    
    // Combinar píxel por píxel
    for (let i = 0; i < maskLength; i++) {
        let pixelValue = 0;
        let contributingMasks = 0;
        
        // Sumar contribuciones de cada máscara disponible
        if (colorMask && i < colorMask.length) {
            const normalizedValue = Array.isArray(colorMask) ? colorMask[i] : colorMask[i] / 255;
            pixelValue += normalizedValue * normWeightColor;
            contributingMasks++;
        }
        
        if (edgeMask && i < edgeMask.length) {
            const normalizedValue = Array.isArray(edgeMask) ? edgeMask[i] : edgeMask[i] / 255;
            pixelValue += normalizedValue * normWeightEdge;
            contributingMasks++;
        }
        
        if (aiMask && i < aiMask.length) {
            const normalizedValue = Array.isArray(aiMask) ? aiMask[i] : aiMask[i] / 255;
            pixelValue += normalizedValue * normWeightAI;
            contributingMasks++;
        }
        
        // Normalizar resultado final y convertir a 0-255
        if (contributingMasks > 0) {
            combined[i] = Math.min(255, Math.max(0, pixelValue * 255));
        }
    }
    
    const activePixels = combined.filter(v => v > 127).length;
    console.log(`✅ Combinación híbrida completada: ${activePixels} píxeles activos de ${maskLength} totales`);
    
    return combined;
}

// Procesamiento híbrido simplificado
async processHybridSimplified() {
    if (!this.originalImage) {
        alert('⚠️ Primero carga una imagen del copépodo');
        return;
    }
    
    this.startProcessing('Híbrido ML');
    
    try {
        this.updateProgress(10);
        
        // Ejecutar técnicas que falten (sin cambiar UI)
        const originalProcessing = this.isProcessing;
        
        if (!this.processedResults['color-segmentation']) {
            console.log('🎯 Ejecutando segmentación por color...');
            this.isProcessing = false;
            await this.processWithColorSegmentation();
        }
        
        if (!this.processedResults['edge-detection']) {
            console.log('🔍 Ejecutando edge detection...');
            this.isProcessing = false;
            await this.processWithEdgeDetection();
        }
        
        if (!this.processedResults['ai-removal']) {
            console.log('🧠 Ejecutando IA avanzada...');
            this.isProcessing = false;
            await this.processWithAI();
        }
        
        // Restaurar estado
        this.isProcessing = originalProcessing;
        this.updateProgress(60);
        
        // Obtener máscaras
        const colorMask = this.processedResults['color-segmentation'];
        const edgeMask = this.processedResults['edge-detection']; 
        const aiMask = this.processedResults['ai-removal'];
        
        if (!colorMask && !edgeMask && !aiMask) {
            throw new Error('No se pudieron generar máscaras base');
        }
        
        // Obtener pesos
        const weightColor = parseFloat(document.getElementById('weight-color').value);
        const weightEdge = parseFloat(document.getElementById('weight-edge').value);
        const weightAI = parseFloat(document.getElementById('weight-ai').value);
        
        console.log(`⚡ Combinando con pesos: Color=${weightColor}, Edge=${weightEdge}, IA=${weightAI}`);
        
        this.updateProgress(75);
        
        // Combinar usando función simplificada
        const combinedMask = this.hybridCombination(colorMask, edgeMask, aiMask, weightColor, weightEdge, weightAI);
        
        this.updateProgress(85);
        
        // Aplicar resultado
        const canvas = document.getElementById('processCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = this.originalImage.width;
        canvas.height = this.originalImage.height;
        ctx.drawImage(this.originalImage, 0, 0);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        
        // Almacenar máscara
        this.processedResults['hybrid'] = combinedMask;
        
        const result = this.applyMask(imageData.data, combinedMask);
        this.displayResult(result, canvas.width, canvas.height, 'hybrid');
        
        this.updateProgress(95);
        
        const accuracy = this.calculateAccuracy(combinedMask);
        this.updateStatus('accuracy', accuracy + '%');
        
        console.log('✅ Procesamiento híbrido completado exitosamente');
        this.finishProcessing();
        
    } catch (error) {
        console.error('❌ Error en procesamiento híbrido:', error);
        alert('❌ Error: ' + error.message);
        this.finishProcessing();
    }
}