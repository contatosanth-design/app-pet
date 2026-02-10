
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aura AI Studio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-deep: #020617;
            --accent: #6366f1;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        html, body, #root {
            height: 100%;
            width: 100%;
            overflow: hidden;
            background-color: var(--bg-deep);
            color: #f8fafc;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .glass-panel {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 5px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #1e293b;
            border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: #334155;
        }
        @keyframes fade-in {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
            animation: fade-in 0.4s ease-out forwards;
        }
    </style>
    <script type="importmap">
{
  "imports": {
    "react": "https://esm.sh/react@19.0.0",
    "react-dom": "https://esm.sh/react-dom@19.0.0",
    "react-dom/client": "https://esm.sh/react-dom@19.0.0/client",
    "react-router-dom": "https://esm.sh/react-router-dom@7.1.0",
    "@google/genai": "https://esm.sh/@google/genai@1.4.0",
    "react-dom/": "https://esm.sh/react-dom@^19.2.4/",
    "react/": "https://esm.sh/react@^19.2.4/"
  }
}
</script>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="./index.tsx"></script>
</body>
</html>
