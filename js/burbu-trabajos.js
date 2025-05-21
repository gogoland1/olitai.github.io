const jobProfiles = [
    {
        title: "Especialista en Modelamiento de Ecosistemas Marinos",
        profile: "Científico con doctorado o maestría en oceanografía, biología marina o ecología, con fuertes habilidades en modelamiento matemático y simulación.",
        function: "Desarrollar y aplicar modelos predictivos para entender cómo las diferentes medidas de gestión pesquera y el cambio climático afectan las poblaciones de peces y el ecosistema marino en su conjunto."
    },
    {
        title: "Genetista de Poblaciones Pesqueras",
        profile: "Biólogo o genetista con especialización en genética de poblaciones.",
        function: "Utilizar herramientas genéticas para identificar stocks pesqueros, evaluar la diversidad genética, el flujo génico entre poblaciones y el impacto de la pesca en la estructura genética, fundamental para definir unidades de manejo."
    },
    {
        title: "Analista de Datos de Desembarques y Esfuerzo Pesquero",
        profile: "Estadístico, ingeniero o científico de datos con experiencia en el manejo y análisis de grandes volúmenes de datos.",
        function: "Recopilar, procesar y analizar datos de desembarques, esfuerzo de pesca, y composición de capturas para evaluar el estado de las pesquerías y el cumplimiento de las cuotas."
    },
    {
        title: "Economista Pesquero",
        profile: "Economista con especialización en recursos naturales o economía pesquera.",
        function: "Analizar la viabilidad económica de las diferentes pesquerías, evaluar el impacto de las regulaciones en la rentabilidad de la industria y proponer esquemas de manejo costo-efectivos."
    },
    {
        title: "Sociólogo Pesquero / Antropólogo Marino",
        profile: "Científico social con experiencia en comunidades costeras y conocimiento de la dinámica sociocultural de la pesca.",
        function: "Estudiar los aspectos sociales, culturales y económicos de las comunidades pesqueras, y cómo las políticas de manejo afectan sus medios de vida y bienestar."
    },
    {
        title: "Especialista en Evaluación de Stock",
        profile: "Científico pesquero con experiencia en modelos de evaluación de poblaciones de peces (e.g., modelos de producción, edad-estructurados, bayesianos).",
        function: "Aplicar modelos matemáticos y estadísticos para estimar la abundancia de las poblaciones de peces, la mortalidad por pesca y los puntos de referencia biológicos para la gestión."
    },
    {
        title: "Oficial de Cumplimiento y Fiscalización Pesquera",
        profile: "Profesional con formación en derecho, ciencias marinas o gestión de recursos naturales, con conocimiento de la normativa pesquera.",
        function: "Vigilar el cumplimiento de las regulaciones pesqueras en el mar y en los puntos de desembarque, incluyendo inspecciones, control de cuotas y combate a la pesca ilegal."
    },
    {
        title: "Desarrollador de Software para Monitoreo Pesquero",
        profile: "Ingeniero de software o desarrollador con experiencia en sistemas de información geográfica (SIG) y bases de datos.",
        function: "Crear y mantener plataformas de software para el seguimiento satelital de embarcaciones (VMS), sistemas de declaración electrónica de capturas (bitácoras electrónicas) y herramientas de análisis de datos."
    },
    {
        title: "Especialista en Artes y Selectividad de Pesca",
        profile: "Ingeniero pesquero o biólogo con conocimiento práctico y teórico de diferentes artes de pesca y su impacto en el ecosistema.",
        function: "Investigar y promover el uso de artes de pesca más selectivas que minimicen la captura incidental de especies no objetivo y el impacto en el hábitat marino."
    },
    {
        title: "Oceanógrafo Físico Aplicado a Pesquerías",
        profile: "Oceanógrafo con experiencia en la modelización de corrientes, frentes y otras características oceanográficas.",
        function: "Analizar cómo las condiciones oceanográficas (temperatura, salinidad, corrientes, surgencias) afectan la distribución y abundancia de los recursos pesqueros y la eficiencia de las operaciones de pesca."
    },
    {
        title: "Biólogo Marino de Campo para Muestreo Biológico",
        profile: "Biólogo marino o técnico con experiencia en muestreo en el mar, identificación de especies y recolección de datos biológicos.",
        function: "Participar en cruceros de investigación para recolectar muestras de peces (e.g., otolitos para edad, gónadas para reproducción, tejido para genética) y datos del ambiente marino."
    },
    {
        title: "Técnico en Acústica Pesquera",
        profile: "Técnico o ingeniero con formación en el uso de ecosondas y software de análisis acústico para la estimación de biomasa de peces.",
        function: "Operar equipos acústicos a bordo de buques de investigación y analizar los datos para estimar la abundancia y distribución de cardúmenes de peces pelágicos."
    },
    {
        title: "Analista GIS para Ordenamiento Espacial Marino",
        profile: "Geógrafo o especialista en SIG con experiencia en análisis espacial y cartografía.",
        function: "Utilizar herramientas SIG para mapear la distribución de recursos, esfuerzo pesquero, áreas de veda, y otros usos del espacio marino, apoyando la planificación y el ordenamiento espacial."
    },
    {
        title: "Especialista en Cambio Climático y Pesquerías",
        profile: "Científico con experiencia en modelado del cambio climático y su impacto en los ecosistemas marinos.",
        function: "Evaluar los efectos del cambio climático (e.g., acidificación, calentamiento, desoxigenación) en las poblaciones de peces y proponer medidas de adaptación para las pesquerías."
    },
    {
        title: "Comunicador Científico y Educador Marino",
        profile: "Profesional con habilidades de comunicación y pasión por la divulgación de la ciencia marina.",
        function: "Traducir los resultados de la investigación pesquera y la complejidad del manejo a un lenguaje accesible para pescadores, tomadores de decisiones y el público general."
    },
    {
        title: "Facilitador de Procesos Participativos en Pesca",
        profile: "Profesional con experiencia en mediación, resolución de conflictos y facilitación de talleres con múltiples actores.",
        function: "Diseñar y facilitar procesos de toma de decisiones que involucren a pescadores, científicos, gobierno y otros stakeholders en la co-gestión de las pesquerías."
    },
    {
        title: "Especialista en Certificación y Trazabilidad Pesquera",
        profile: "Profesional con conocimiento de estándares de sostenibilidad (e.g., MSC) y sistemas de trazabilidad de productos pesqueros.",
        function: "Asesorar a las pesquerías en el cumplimiento de los requisitos para obtener certificaciones de sostenibilidad y en la implementación de sistemas que garanticen la legalidad y el origen del producto."
    },
    {
        title: "Observador Científico a Bordo",
        profile: "Técnico o biólogo marino entrenado para registrar datos de captura, esfuerzo y biología a bordo de embarcaciones comerciales.",
        function: "Monitorear las operaciones de pesca comercial, registrar la composición de las capturas (incluyendo especies incidentales), y recolectar muestras biológicas."
    },
    {
        title: "Analista de Riesgo Ecológico para Pesquerías (ERAE)",
        profile: "Científico con experiencia en evaluación de riesgo y conocimiento de los impactos de la pesca en el ecosistema.",
        function: "Aplicar metodologías de ERAE para identificar los componentes del ecosistema más vulnerables a los impactos de una pesquería particular y priorizar acciones de manejo."
    },
    {
        title: "Especialista en Manejo Basado en Ecosistemas (MBE)",
        profile: "Científico o gestor con una visión holística del manejo pesquero, considerando las interacciones entre especies y con el ambiente.",
        function: "Desarrollar e implementar planes de manejo que integren consideraciones ecosistémicas, buscando mantener la salud y productividad de todo el ecosistema marino."
    },
    {
        title: "Técnico en Cultivo de Especies para Repoblación",
        profile: "Biólogo o técnico acuícola con experiencia en reproducción y cultivo de larvas y juveniles de especies marinas.",
        function: "Desarrollar técnicas de cultivo para especies sobreexplotadas con el fin de liberar individuos al medio natural y ayudar a la recuperación de sus poblaciones."
    },
    {
        title: "Especialista en Sensores Remotos y Oceanografía Satelital",
        profile: "Oceanógrafo o geógrafo con experiencia en el procesamiento y análisis de imágenes satelitales (e.g., clorofila-a, TSM, vientos).",
        function: "Utilizar datos satelitales para monitorear las condiciones del océano a gran escala y detectar patrones relevantes para la pesca, como frentes, remolinos o floraciones algales."
    },
    {
        title: "Bioinformático para Análisis Genómicos en Pesca",
        profile: "Científico con habilidades en bioinformática y análisis de datos genómicos y transcriptómicos.",
        function: "Analizar grandes volúmenes de datos genéticos para estudios de estructura poblacional, adaptación local, trazabilidad de productos y detección de fraude."
    },
    {
        title: "Modelador Bioeconómico",
        profile: "Científico con capacidad de integrar modelos biológicos de poblaciones de peces con modelos económicos de comportamiento de flotas pesqueras.",
        function: "Desarrollar modelos que simulen la interacción entre la dinámica de los recursos pesqueros y las decisiones económicas de los pescadores, para evaluar políticas de manejo."
    },
    {
        title: "Especialista en Derecho del Mar y Política Pesquera Internacional",
        profile: "Abogado o internacionalista con especialización en derecho del mar y regímenes de manejo pesquero en aguas internacionales y transzonales.",
        function: "Asesorar en negociaciones internacionales, cumplimiento de acuerdos y desarrollo de políticas para la gestión de recursos compartidos o en alta mar."
    },
    {
        title: "Ingeniero en Robótica Marina para Monitoreo",
        profile: "Ingeniero con experiencia en el diseño y operación de vehículos autónomos submarinos (AUVs) y vehículos operados remotamente (ROVs).",
        function: "Utilizar robots marinos para la recolección de datos oceanográficos, filmación de fondos marinos, inspección de artes de pesca perdidas y monitoreo de áreas marinas protegidas."
    },
    {
        title: "Curador de Datos Oceanográficos y Pesqueros",
        profile: "Profesional con experiencia en gestión de bases de datos, metadatos y estándares de calidad de datos.",
        function: "Organizar, documentar y asegurar la calidad y accesibilidad a largo plazo de los datos recolectados por programas de monitoreo pesquero e investigación oceanográfica."
    },
    {
        title: "Especialista en Contaminación Marina y Pesquerías",
        profile: "Ecotoxicólogo o químico ambiental con conocimiento de los efectos de los contaminantes en los organismos y ecosistemas marinos.",
        function: "Investigar cómo la contaminación por plásticos, metales pesados o compuestos orgánicos persistentes afecta la salud de los recursos pesqueros y la seguridad alimentaria."
    },
    {
        title: "Analista de Redes Tróficas Marinas",
        profile: "Ecólogo cuantitativo con experiencia en el análisis de redes alimentarias y modelos como Ecopath con Ecosim.",
        function: "Modelar las interacciones tróficas en el ecosistema marino para entender cómo la pesca de una especie puede afectar a otras, y evaluar los impactos ecosistémicos del manejo."
    },
    {
        title: "Técnico de Laboratorio para Análisis de Edad y Crecimiento",
        profile: "Técnico con habilidad en la preparación y lectura de estructuras calcificadas (otolitos, escamas, vértebras) para determinar la edad de los peces.",
        function: "Procesar muestras, realizar lecturas de edad y analizar datos de crecimiento que son fundamentales para los modelos de evaluación de stock."
    },
    {
        title: "Especialista en Logística de Cruceros de Investigación",
        profile: "Profesional con experiencia en la planificación y coordinación de operaciones marítimas y campañas científicas.",
        function: "Organizar la logística de los cruceros de investigación, incluyendo la preparación del buque, equipos, permisos, personal y gestión de muestras y datos."
    },
    {
        title: "Hidrogeólogo Costero",
        profile: "Experto en la interacción entre aguas subterráneas y el mar.",
        function: "Estudiar el impacto de las descargas de aguas subterráneas en la calidad del agua costera y los ecosistemas marinos."
    },
    {
        title: "Especialista en Restauración de Hábitats Marinos",
        profile: "Ecólogo con experiencia en técnicas de restauración de arrecifes, praderas marinas o manglares.",
        function: "Diseñar e implementar proyectos para restaurar hábitats marinos degradados y mejorar su función como criaderos de especies pesqueras."
    },
    {
        title: "Analista de Mercados de Productos del Mar",
        profile: "Profesional con conocimiento de las cadenas de valor, precios y tendencias de consumo de pescados y mariscos.",
        function: "Monitorear los mercados nacionales e internacionales para identificar oportunidades para productos pesqueros sostenibles y agregar valor a las capturas."
    },
    {
        title: "Especialista en Seguros para la Actividad Pesquera y Acuícola",
        profile: "Experto en evaluación de riesgos y diseño de productos de seguros adaptados a los desafíos de la pesca y la acuicultura.",
        function: "Desarrollar y ofrecer soluciones de seguros para cubrir riesgos asociados a fenómenos climáticos, enfermedades en acuicultura o accidentes en el mar."
    },
    {
        title: "Auditor de Sostenibilidad Pesquera",
        profile: "Profesional con experiencia en la aplicación de estándares de auditoría y conocimiento de los criterios de sostenibilidad pesquera.",
        function: "Realizar auditorías independientes para verificar el cumplimiento de los estándares de certificación pesquera (e.g., MSC) por parte de las pesquerías."
    },
    {
        title: "Instructor de Buceo Científico y Técnico",
        profile: "Buzo experimentado con certificaciones para instruir en técnicas de muestreo y seguridad en buceo científico.",
        function: "Capacitar a científicos y técnicos en métodos de investigación subacuática y protocolos de buceo seguro."
    },
    {
        title: "Cartógrafo Náutico Digital",
        profile: "Especialista en la creación y actualización de cartas náuticas electrónicas.",
        function: "Integrar datos batimétricos, oceanográficos y de ayudas a la navegación para producir cartas digitales precisas para la navegación segura."
    },
    {
        title: "Especialista en Manejo Integrado de Zonas Costeras (MIZC)",
        profile: "Planificador o gestor con experiencia en la coordinación de múltiples usos y usuarios en la zona costera.",
        function: "Facilitar procesos de planificación para armonizar el desarrollo de actividades como la pesca, acuicultura, turismo y conservación en la franja costera."
    },
    {
        title: "Técnico en Mantenimiento de Equipos Oceanográficos",
        profile: "Electrónico o técnico instrumental con experiencia en la calibración y reparación de sensores y equipos de muestreo marino.",
        function: "Asegurar el correcto funcionamiento de los instrumentos oceanográficos (CTDs, ADCPs, ecosondas, etc.) a través de mantenimiento preventivo y correctivo."
    },
    {
        title: "Especialista en Valorización de Subproductos Pesqueros",
        profile: "Ingeniero en alimentos, químico o biotecnólogo con ideas innovadoras para el aprovechamiento de partes del pescado que normalmente se descartan.",
        function: "Investigar y desarrollar nuevos productos (e.g., colágeno, aceites omega-3, harina de pescado de alto valor) a partir de subproductos de la pesca y la acuicultura."
    },
    {
        title: "Paleoceanógrafo",
        profile: "Científico que estudia los océanos del pasado.",
        function: "Analizar sedimentos marinos y otros registros geológicos para reconstruir las condiciones oceánicas pasadas y entender cambios climáticos a largo plazo."
    },
    {
        title: "Especialista en Acuicultura Multitrófica Integrada (AMTI)",
        profile: "Acuicultor o biólogo marino con visión de sistemas para el cultivo combinado de diferentes especies.",
        function: "Diseñar y operar sistemas de AMTI donde los desechos de una especie son aprovechados como alimento por otra, minimizando el impacto ambiental y diversificando la producción."
    },
    {
        title: "Operador de Drones para Monitoreo Costero y Marino",
        profile: "Piloto de dron certificado con experiencia en la captura de imágenes aéreas y videos en ambientes marinos.",
        function: "Utilizar drones equipados con diferentes sensores para el monitoreo de poblaciones de aves y mamíferos marinos, detección de floraciones algales, inspección de infraestructura costera o vigilancia contra pesca ilegal."
    },
    {
        title: "Especialista en Bio-óptica Marina",
        profile: "Físico u oceanógrafo que estudia cómo la luz interactúa con el agua y los organismos marinos.",
        function: "Utilizar mediciones de las propiedades ópticas del agua para estimar concentraciones de fitoplancton, materia orgánica disuelta y sedimentos, y para calibrar sensores satelitales."
    },
    {
        title: "Analista de Políticas de Adaptación al Cambio Climático en Zonas Costeras",
        profile: "Cientista político, sociólogo o geógrafo con enfoque en gobernanza y políticas públicas para la adaptación.",
        function: "Evaluar la efectividad de las políticas existentes y proponer nuevas estrategias para ayudar a las comunidades costeras y los ecosistemas marinos a adaptarse a los impactos del cambio climático."
    },
    {
        title: "Taxónomo de Especies Marinas (Clásico y Molecular)",
        profile: "Biólogo con profundo conocimiento en la identificación y clasificación de organismos marinos, utilizando tanto morfología como herramientas moleculares.",
        function: "Identificar y describir la biodiversidad marina, incluyendo nuevas especies, y mantener colecciones de referencia y bases de datos taxonómicas actualizadas."
    },
    {
        title: "Ingeniero de Energías Renovables Marinas",
        profile: "Ingeniero especializado en el diseño e implementación de tecnologías para obtener energía de las olas, mareas o gradientes térmicos del océano.",
        function: "Desarrollar proyectos de energía marina, evaluando su factibilidad técnica, económica y ambiental, y su posible impacto en los ecosistemas y pesquerías."
    },
    {
        title: "Especialista en Sonido y Bioacústica Marina",
        profile: "Científico que estudia los sonidos producidos por los animales marinos y el impacto del ruido antropogénico.",
        function: "Utilizar hidrófonos para monitorear poblaciones de mamíferos marinos, estudiar su comportamiento acústico y evaluar cómo el ruido de barcos o sonares afecta su comunicación y salud."
    },
    {
        title: "Geoquímico Marino",
        profile: "Químico u oceanógrafo que estudia los ciclos de los elementos químicos en el océano.",
        function: "Analizar la composición química del agua de mar, sedimentos y organismos para entender procesos como la acidificación oceánica, los ciclos de nutrientes y la contaminación."
    },
    {
        title: "Planificador de Áreas Marinas Protegidas (AMP)",
        profile: "Ecólogo, geógrafo o gestor ambiental con experiencia en diseño y manejo de AMPs.",
        function: "Utilizar información científica y socioeconómica para proponer la creación de nuevas AMPs, definir sus objetivos de conservación y zonificación, y desarrollar planes de manejo efectivos."
    },
    {
        title: "Especialista en Turismo Marino Sostenible",
        profile: "Profesional del turismo con enfoque en la conservación y el desarrollo de experiencias de bajo impacto.",
        function: "Diseñar y promover actividades turísticas (e.g., avistamiento de ballenas, buceo en arrecifes) que sean respetuosas con el medio ambiente marino y beneficien a las comunidades locales."
    },
    {
        title: "Meteorólogo Marino / Pronosticador de Oleaje",
        profile: "Meteorólogo con especialización en la predicción de condiciones atmosféricas y de oleaje en el mar.",
        function: "Generar pronósticos precisos de vientos, olas y corrientes para la seguridad de la navegación, operaciones pesqueras y actividades costeras."
    },
    {
        title: "Especialista en Biorremediación Marina",
        profile: "Microbiólogo o biotecnólogo que utiliza organismos vivos para limpiar contaminantes del agua de mar o sedimentos.",
        function: "Investigar y aplicar el uso de bacterias, algas u otros organismos para degradar derrames de petróleo, exceso de nutrientes u otros contaminantes en el medio marino."
    },
    {
        title: "Abogado Ambientalista Marino",
        profile: "Abogado especializado en legislación ambiental y litigación para la protección de los ecosistemas marinos.",
        function: "Representar a organizaciones o comunidades en casos legales relacionados con daños ambientales al océano, pesca ilegal o incumplimiento de normativas de conservación."
    },
    {
        title: "Ilustrador Científico Marino",
        profile: "Artista con habilidad para representar con precisión y detalle organismos y procesos marinos.",
        function: "Crear ilustraciones para publicaciones científicas, material educativo, museos y acuarios, ayudando a visualizar la vida marina y los conceptos oceanográficos."
    },
    {
        title: "Especialista en Ciencia Ciudadana Marina",
        profile: "Coordinador con habilidades para involucrar al público en la recolección de datos científicos sobre el océano.",
        function: "Diseñar y gestionar proyectos donde buzos recreativos, pescadores o playeros recolectan información valiosa sobre especies, basura marina o cambios en la costa."
    },
    {
        title: "Técnico en Manejo de Datos de Boyas Oceanográficas",
        profile: "Técnico con experiencia en la adquisición, control de calidad y transmisión de datos de sensores en boyas fijas o derivantes.",
        function: "Mantener y operar redes de boyas oceanográficas que recolectan datos en tiempo real sobre variables atmosféricas y oceánicas."
    },
    {
        title: "Especialista en Arqueología Subacuática",
        profile: "Arqueólogo entrenado en técnicas de excavación y conservación de sitios y artefactos sumergidos.",
        function: "Descubrir, investigar y proteger el patrimonio cultural subacuático, como naufragios antiguos o asentamientos costeros prehistóricos."
    },
    {
        title: "Consultor en Manejo de Crisis por Derrames de Hidrocarburos",
        profile: "Experto en la respuesta a emergencias ambientales y planes de contingencia para derrames de petróleo en el mar.",
        function: "Asesorar a gobiernos y empresas en la preparación y ejecución de planes para prevenir, contener y limpiar derrames de hidrocarburos y minimizar su impacto ambiental."
    },
    {
        title: "Científico de Datos para Optimización de Rutas de Navegación",
        profile: "Analista de datos con habilidades en modelado y optimización.",
        function: "Utilizar datos de corrientes, vientos, mareas y consumo de combustible para optimizar las rutas de buques mercantes y reducir emisiones."
    },
    {
        title: "Especialista en Comunicación de Riesgos Costeros",
        profile: "Comunicador social o geógrafo con experiencia en la difusión de información sobre peligros como tsunamis, marejadas o erosión costera.",
        function: "Desarrollar estrategias y materiales para informar a las comunidades costeras sobre los riesgos a los que están expuestas y las medidas de preparación y evacuación."
    },
    {
        title: "Gestor de Programas de Pesca de Pequeña Escala",
        profile: "Profesional con experiencia en el trabajo con organizaciones de pescadores artesanales y en el desarrollo de proyectos productivos sostenibles.",
        function: "Apoyar a comunidades de pescadores artesanales en la mejora de sus prácticas de pesca, la diversificación de sus ingresos y el fortalecimiento de su gobernanza."
    },
    {
        title: "Especialista en Carbono Azul",
        profile: "Ecólogo o científico ambiental enfocado en la capacidad de los ecosistemas costeros (manglares, marismas, pastos marinos) para secuestrar carbono.",
        function: "Medir y modelar el secuestro de carbono por estos ecosistemas y promover su conservación y restauración como una estrategia de mitigación del cambio climático."
    },
    {
        title: "Analista de Imágenes de Pláncton Asistido por IA",
        profile: "Biólogo u oceanógrafo con experiencia en el uso de sistemas de imagen (e.g., FlowCam, ZooScan) y algoritmos de IA para el análisis de muestras de pláncton.",
        function: "Procesar y analizar grandes cantidades de imágenes de pláncton para identificar especies, estimar biomasas y detectar cambios en las comunidades planctónicas de forma rápida y precisa."
    },
    {
        title: "Especialista en Acuicultura Oceánica (Offshore)",
        profile: "Ingeniero acuícola o naval con experiencia en el diseño y operación de sistemas de cultivo en mar abierto.",
        function: "Desarrollar y gestionar proyectos de acuicultura lejos de la costa, utilizando estructuras robustas y tecnologías avanzadas para minimizar el impacto ambiental y los conflictos de uso."
    },
    {
        title: "Bioestadístico Marino",
        profile: "Estadístico con experiencia en el diseño experimental y análisis de datos biológicos y ecológicos en el contexto marino.",
        function: "Asesorar a investigadores en el diseño de estudios, análisis de datos y la interpretación de resultados, aplicando modelos estadísticos apropiados a la complejidad de los datos marinos."
    },
    {
        title: "Coordinador de Redes de Varamientos de Fauna Marina",
        profile: "Biólogo o veterinario con experiencia en la atención de animales marinos varados y en la coordinación de equipos de respuesta.",
        function: "Gestionar una red de voluntarios y profesionales para responder a eventos de varamiento de ballenas, delfines, tortugas o aves marinas, recolectando datos y asistiendo a los animales."
    },
    {
        title: "Especialista en Diplomacia Científica Oceánica",
        profile: "Científico o diplomático con habilidades para facilitar la colaboración internacional en investigación y conservación marina.",
        function: "Promover la cooperación científica y el desarrollo de políticas basadas en ciencia entre países para abordar problemas oceánicos transfronterizos como la sobrepesca o la contaminación."
    },
    {
        title: "Técnico de Soporte Informático para Plataformas de Datos Oceanográficos",
        profile: "Apoyo a infraestructura digital",
        function: "Mantenimiento de servidores, software especializado y apoyo a usuarios de plataformas de datos."
    }
];

document.addEventListener('DOMContentLoaded', () => {
    const bubbleArea = document.getElementById('bubble-area');
    if (!bubbleArea) {
        console.error('Bubble area not found!');
        return;
    }

    // Modal elements
    const modal = document.getElementById('jobModal');
    const modalJobTitle = document.getElementById('modalJobTitle');
    const modalJobProfile = document.getElementById('modalJobProfile');
    const modalJobFunction = document.getElementById('modalJobFunction');
    const closeButton = document.querySelector('.close-button');

    if (!modal || !closeButton || !modalJobTitle || !modalJobProfile || !modalJobFunction) {
        console.error('Modal elements not found!');
        return;
    }

    jobProfiles.forEach(job => {
        const bubble = document.createElement('div');
        bubble.classList.add('job-bubble');
        
        bubble.textContent = job.title.substring(0, 30) + (job.title.length > 30 ? '...' : ''); 
        
        bubble.dataset.profile = job.profile;
        bubble.dataset.function = job.function;
        bubble.dataset.title = job.title; 

        const bubbleSize = 120; 
        const areaHeight = bubbleArea.clientHeight || 600; 
        const areaWidth = bubbleArea.clientWidth || bubbleArea.offsetWidth; 

        const topPos = Math.random() * Math.max(0, areaHeight - bubbleSize);
        const leftPos = Math.random() * Math.max(0, areaWidth - bubbleSize);
        
        bubble.style.top = `${topPos}px`;
        bubble.style.left = `${leftPos}px`;

        // Add random animation delay and potentially duration
        const randomDelay = Math.random() * 15; // Random delay up to 15 seconds
        bubble.style.animationDelay = `-${randomDelay}s`; // Negative delay starts partway through
        
        const randomDuration = 12 + Math.random() * 8; // Duration between 12s and 20s
        bubble.style.animationDuration = `${randomDuration}s`;

        bubble.addEventListener('click', () => {
            modalJobTitle.textContent = job.title; 
            modalJobProfile.textContent = job.dataset.profile;
            modalJobFunction.textContent = job.dataset.function;
            modal.style.display = 'block';
        });

        bubbleArea.appendChild(bubble);
    });

    closeButton.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });
});
