# LoL Personal Counter-Pick Engine

A dynamic League of Legends application that analyzes player match history and champion mastery to provide intelligent counter-pick recommendations using the official Riot Games API.

## 🎯 Features

- **Real-time Data Analysis**: Fetches live player data from Riot Games API
- **Champion Mastery Integration**: Analyzes your top 15 most played champions
- **Match History Analysis**: Reviews your last 20 games for performance metrics
- **Intelligent Scoring**: Combines global win rates, personal mastery, and recent performance
- **Dynamic Recommendations**: Shows which champions from YOUR pool counter the enemy pick
- **Multi-Region Support**: Works with all major League of Legends regions

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Riot Games API Key ([Get one here](https://developer.riotgames.com/))

### Installation

1. **Clone the repository**
```bash
cd c:\Users\steam\OneDrive\Masaüstü\riotapi
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure API Key**

Edit `backend/.env`:
```env
RIOT_API_KEY=RGAPI-your-api-key-here
RATE_LIMIT_PER_SECOND=20
RATE_LIMIT_PER_TWO_MINUTES=100
```

4. **Start Backend**
```bash
python main.py
```
Backend runs at: `http://localhost:8000`

5. **Frontend Setup**
```bash
cd ../frontend
npm install
npm run dev
```
Frontend runs at: `http://localhost:5173`

## 📖 Usage

1. Open `http://localhost:5173` in your browser
2. Enter your Riot ID (e.g., `Faker#T1`)
3. Select your region
4. Enter the enemy champion name (e.g., `Darius`)
5. Click "Find Counter-Picks"

The app will show you:
- **Best counter-picks** from your champion pool
- **Suitability Score** (0-100)
- **Global Win Rate** against the target
- **Your Mastery Points** on each champion
- **Recent Performance** (win rate from last 20 games)

## 🏗️ Architecture

### Backend (FastAPI)
- `main.py` - API endpoints and request handling
- `riot_client.py` - Riot Games API integration
- `scoring.py` - Intelligent scoring algorithm
- `models.py` - Pydantic data models

### Frontend (React + Vite)
- Modern React 18 with hooks
- Tailwind CSS for styling
- Axios for API calls
- Framer Motion for animations

### Scoring Algorithm

The recommendation score is calculated using three weighted factors:

1. **Global Win Rate (45%)**: How well the champion performs against the target globally
2. **Mastery Points (35%)**: Your experience with the champion (logarithmic scale)
3. **Recent Performance (20%)**: Your win rate with the champion in recent games

Formula:
```
Score = (Global_WR × 0.45) + (Mastery_Score × 0.35) + (Recent_WR × 0.20)
```

## 🔧 API Endpoints

### `GET /`
Health check endpoint

**Response:**
```json
{
  "message": "LPC-Engine Backend [Real Riot API] is Running",
  "status": "ready"
}
```

### `POST /recommend`
Get counter-pick recommendations

**Request:**
```json
{
  "summoner_name": "Faker",
  "tag_line": "T1",
  "region": "kr",
  "target_champion": "Zed"
}
```

**Response:**
```json
{
  "target_champion": "Zed",
  "recommendations": [
    {
      "champion_id": "Malphite",
      "champion_name": "Malphite",
      "score": 78.5,
      "details": {
        "global_wr": 0.56,
        "mastery": 250000,
        "recent_wr": 0.65
      }
    }
  ]
}
```

## 🌍 Supported Regions

- TR - Turkey (`tr1`)
- EUW - West Europe (`euw1`)
- EUNE - Nordic & East (`eun1`)
- NA - North America (`na1`)
- BR - Brazil (`br1`)
- LAN - Latin America North (`la1`)
- LAS - Latin America South (`la2`)
- KR - Korea (`kr`)
- JP - Japan (`jp1`)

## 🐛 Troubleshooting

### Backend Issues

**"RIOT_API_KEY not found"**
- Check your `.env` file has the correct API key

**"ModuleNotFoundError"**
- Run `pip install -r requirements.txt`

### Frontend Issues

**"Cannot find module 'react'"**
- Run `npm install`

**"Port already in use"**
- Use a different port: `npm run dev -- --port 3000`

### API Issues

**"Account not found"**
- Verify Riot ID format: `Name#TAG`
- Check you selected the correct region

**"Rate limited"**
- Development API keys have limits (20/sec, 100/2min)
- Wait a few moments or apply for a production key

## 📝 Project Structure

```
riotapi/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── riot_client.py       # Riot API client
│   ├── scoring.py           # Scoring engine
│   ├── models.py            # Data models
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # API configuration
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Tailwind styles
│   ├── index.html           # HTML template
│   ├── package.json         # Node dependencies
│   ├── tailwind.config.js   # Tailwind config
│   └── vite.config.js       # Vite config
│
├── README.md               # This file
└── KURULUM.md             # Turkish setup guide
```

## 🔐 Security Notes

- Never commit `.env` files to version control
- Add `.env` to `.gitignore`
- Use environment variables in production
- Rotate API keys regularly

## 🚀 Future Enhancements

- [ ] Integration with U.GG/OP.GG for real-time counter data
- [ ] Redis caching for API responses
- [ ] User authentication and preferences
- [ ] Multi-role analysis (Top, Jungle, Mid, ADC, Support)
- [ ] Rank-based recommendations
- [ ] Team composition analysis
- [ ] Meta trend tracking

## 📚 Resources

- [Riot Developer Portal](https://developer.riotgames.com/)
- [Riot API Documentation](https://developer.riotgames.com/apis)
- [Data Dragon](https://developer.riotgames.com/docs/lol#data-dragon)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

## 📄 License

This project is for educational purposes. Riot Games API usage must comply with their [Terms of Service](https://developer.riotgames.com/terms).

## 🎮 Enjoy!

Happy counter-picking! May your LP gains be plentiful! 🏆
