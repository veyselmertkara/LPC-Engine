import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
    const [summonerName, setSummonerName] = useState('')
    const [targetChampion, setTargetChampion] = useState('')
    const [region, setRegion] = useState('tr1')
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    useEffect(() => {
        const particles = document.querySelector('.particles')
        if (!particles) return

        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div')
            particle.className = 'particle'
            particle.style.left = Math.random() * 100 + '%'
            particle.style.animationDelay = Math.random() * 10 + 's'
            particles.appendChild(particle)
        }
    }, [])

    const handleAnalyze = async () => {
        if (!summonerName || !targetChampion) return
        setLoading(true)
        setError(null)
        setData(null)

        let [name, tag] = summonerName.split('#')
        if (!tag) tag = "TR1"

        try {
            const response = await axios.post('http://localhost:8000/recommend', {
                summoner_name: name.trim(),
                tag_line: tag.trim(),
                region: region,
                target_champion: targetChampion
            })
            setData(response.data)
        } catch (err) {
            console.error(err)
            setError(err.response?.data?.detail ? JSON.stringify(err.response.data.detail) : "Failed to fetch recommendations.")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen relative z-10 flex flex-col items-center p-8">
            <div className="particles"></div>

            <header className="mb-16 text-center relative">
                <h1 className="text-7xl font-black gradient-text mb-4" style={{ fontFamily: "'Orbitron', sans-serif" }}>
                    LPC ENGINE
                </h1>
                <div className="h-1 w-32 mx-auto bg-gradient-to-r from-transparent via-electric-blue to-transparent glow"></div>
                <p className="text-gray-400 mt-4 text-lg tracking-widest uppercase">League Personal Counter</p>
            </header>

            <div className="w-full max-w-3xl glass-effect p-10 rounded-2xl glow mb-12 relative">
                <div className="relative z-10">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div>
                            <label className="block text-xs font-bold text-electric-blue uppercase mb-2 tracking-wider">Summoner Name</label>
                            <input
                                type="text"
                                value={summonerName}
                                onChange={(e) => setSummonerName(e.target.value)}
                                placeholder="Faker#T1"
                                className="w-full bg-black/50 border-2 border-electric-blue/30 rounded-lg p-4 text-white focus:border-electric-blue focus:outline-none transition-all duration-300 hover:border-electric-blue/50"
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-bold text-electric-blue uppercase mb-2 tracking-wider">Region</label>
                            <select
                                value={region}
                                onChange={(e) => setRegion(e.target.value)}
                                className="w-full bg-black/50 border-2 border-electric-blue/30 rounded-lg p-4 text-white focus:border-electric-blue focus:outline-none transition-all duration-300 hover:border-electric-blue/50 cursor-pointer"
                            >
                                <option value="tr1">TR - Turkey</option>
                                <option value="euw1">EUW - West Europe</option>
                                <option value="eun1">EUNE - Nordic & East</option>
                                <option value="na1">NA - North America</option>
                                <option value="kr">KR - Korea</option>
                                <option value="jp1">JP - Japan</option>
                            </select>
                        </div>
                    </div>

                    <div className="mb-6">
                        <label className="block text-xs font-bold text-electric-blue uppercase mb-2 tracking-wider">Target Enemy</label>
                        <input
                            type="text"
                            value={targetChampion}
                            onChange={(e) => setTargetChampion(e.target.value)}
                            placeholder="Yasuo"
                            onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
                            className="w-full bg-black/50 border-2 border-electric-blue/30 rounded-lg p-4 text-white focus:border-electric-blue focus:outline-none transition-all duration-300 hover:border-electric-blue/50"
                        />
                    </div>

                    <button
                        onClick={handleAnalyze}
                        disabled={loading}
                        className={`w-full py-5 rounded-lg premium-button text-xl ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                    >
                        {loading ? 'ANALYZING...' : 'FIND COUNTER-PICKS'}
                    </button>

                    {error && (
                        <div className="mt-6 p-4 bg-red-900/30 border-2 border-red-500 text-red-200 rounded-lg text-center">
                            {error}
                        </div>
                    )}
                </div>
            </div>

            {data && (
                <div className="w-full max-w-7xl animate-fade-in-up">
                    <div className="text-center mb-10">
                        <span className="text-gray-400 text-lg">Counter picks for</span>
                        <span className="text-red-500 font-black ml-3 text-4xl" style={{ fontFamily: "'Bebas Neue', sans-serif" }}>{data.target_champion}</span>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        <div>
                            <h2 className="text-2xl font-black text-electric-blue mb-6 flex items-center gap-3" style={{ fontFamily: "'Bebas Neue', sans-serif" }}>
                                <span className="text-3xl">🌍</span>
                                <span>Global Best Counters</span>
                            </h2>
                            <div className="space-y-4">
                                {data.global_counters.map((counter, index) => (
                                    <GlobalCounterCard key={counter.champion_name} data={counter} rank={index + 1} />
                                ))}
                            </div>
                        </div>

                        <div>
                            <h2 className="text-2xl font-black text-electric-blue mb-6 flex items-center gap-3" style={{ fontFamily: "'Bebas Neue', sans-serif" }}>
                                <span className="text-3xl">⭐</span>
                                <span>Your Champion Pool</span>
                            </h2>
                            <div className="space-y-4">
                                {data.user_pool_recommendations.length > 0 ? (
                                    data.user_pool_recommendations.map((rec, index) => (
                                        <UserPoolCard key={rec.champion_id} data={rec} rank={index + 1} />
                                    ))
                                ) : (
                                    <div className="glass-effect p-8 rounded-lg text-center text-gray-400">
                                        No champions from your pool found
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

function GlobalCounterCard({ data, rank }) {
    const championImageUrl = `https://ddragon.leagueoflegends.com/cdn/14.24.1/img/champion/${data.champion_name.replace(/[^a-zA-Z]/g, '')}.png`

    return (
        <div className="relative" style={{ overflow: 'visible' }}>
            <div className={`glass-effect p-5 rounded-xl border-2 flex items-center gap-4 transition-all duration-300 hover:scale-105
                ${data.in_user_pool ? 'border-green-400/50 glow-blue' : 'border-electric-blue/20 hover:border-electric-blue/40'}`}>

                {data.in_user_pool && (
                    <div className="absolute -top-3 -right-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white text-xs font-black px-3 py-2 rounded-md shadow-xl z-50">
                        ✓ IN POOL
                    </div>
                )}

                <div className="flex-shrink-0 w-14 h-14 rounded-full overflow-hidden border-2 border-electric-blue/50 glow">
                    <img src={championImageUrl} alt={data.champion_name} className="w-full h-full object-cover" />
                </div>

                <div className="flex-grow">
                    <h3 className="text-xl font-bold text-white">{data.champion_name}</h3>
                    <div className="text-xs text-gray-500 uppercase">Rank #{rank}</div>
                </div>

                <div className="text-right">
                    <div className="text-3xl font-black text-electric-blue leading-none">{(data.win_rate * 100).toFixed(1)}%</div>
                    <div className="text-[10px] text-gray-500 uppercase mt-1">Win Rate</div>
                </div>
            </div>
        </div>
    )
}

function UserPoolCard({ data, rank }) {
    const isTopPick = rank === 1
    const championImageUrl = `https://ddragon.leagueoflegends.com/cdn/14.24.1/img/champion/${data.champion_name.replace(/[^a-zA-Z]/g, '')}.png`

    return (
        <div className="relative" style={{ overflow: 'visible' }}>
            <div className={`glass-effect p-5 rounded-xl border-2 flex items-center gap-4 transition-all duration-300 hover:scale-105
                ${isTopPick ? 'border-yellow-500/50 glow' : 'border-electric-blue/20 hover:border-electric-blue/40'}`}>

                {isTopPick && (
                    <div className="absolute -top-3 -left-3 bg-gradient-to-r from-yellow-500 to-orange-600 text-black text-xs font-black px-4 py-2 rounded-md shadow-xl z-50">
                        ★ BEST BET
                    </div>
                )}

                <div className="flex-shrink-0 w-14 h-14 rounded-full overflow-hidden border-2 border-electric-blue/50 glow">
                    <img src={championImageUrl} alt={data.champion_name} className="w-full h-full object-cover" />
                </div>

                <div className="flex-grow">
                    <h3 className={`text-xl font-bold ${isTopPick ? 'text-yellow-400' : 'text-white'}`}>{data.champion_name}</h3>
                    <div className="flex gap-3 mt-1 text-xs text-gray-400 uppercase">
                        <span>WR: <span className="text-gray-200">{(data.details.global_wr * 100).toFixed(1)}%</span></span>
                        <span>Mastery: <span className="text-gray-200">{(data.details.mastery / 1000).toFixed(0)}k</span></span>
                    </div>
                </div>

                <div className="text-right">
                    <div className={`text-3xl font-black leading-none ${isTopPick ? 'text-yellow-400' : 'text-electric-blue'}`}>{data.score}</div>
                    <div className="text-[10px] text-gray-500 uppercase mt-1">Score</div>
                </div>
            </div>
        </div>
    )
}

export default App
