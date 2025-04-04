# Visual Search using CLIP

This project implements a visual search system using OpenAI's CLIP model. The backend is built with FastAPI, and the frontend is developed using React.js.

## Features
✅ Upload images to the backend
✅ Search for similar images using text queries
✅ Uses FAISS for efficient image retrieval

---

## 🛠 Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-username/vlm-visual-search.git
cd vlm-visual-search
```

### 2️⃣ Install Backend Dependencies
```sh
cd backend
pip install -r requirements.txt
```

### 3️⃣ Start Backend Server
```sh
uvicorn main:app --reload
```

### 4️⃣ Install Frontend Dependencies
```sh
cd ../frontend
npm install
```

### 5️⃣ Start Frontend
```sh
npm start
```

---

## 🚀 API Endpoints
### 📌 Upload an Image
```
POST /upload/
```
- Uploads an image and extracts its embedding.

### 📌 Search for Images
```
GET /search/?query=<text>
```
- Searches for images matching a text description.

---

## 📦 Deployment
You can deploy the backend using **Docker**:
```sh
cd backend
docker build -t vlm-backend .
docker run -p 8000:8000 vlm-backend
```
For frontend deployment, use **Vercel** or **Netlify**.

---

## 📝 License
This project is licensed under the MIT License.

---

Need help? Open an issue! 🚀
