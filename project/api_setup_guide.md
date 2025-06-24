# 🚀 Advanced Jarvis - API Setup Guide

## Required API Keys

To unlock the full potential of your Advanced Jarvis AI Assistant, you'll need to set up several API keys. Here's how to get them:

### 1. 🧠 OpenAI API Key (Essential for AI Features)

**What it enables:** Intelligent conversations, context awareness, smart responses

**How to get it:**
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to "API Keys" section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)

**Cost:** Pay-per-use, very affordable for personal use (~$0.002 per 1K tokens)

### 2. 🌤️ OpenWeatherMap API Key (Weather Features)

**What it enables:** Real-time weather information for any city

**How to get it:**
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Go to "My API Keys" section
4. Copy your default API key

**Cost:** Free tier includes 1,000 calls/day

### 3. 📰 News API Key (News Features)

**What it enables:** Latest news from thousands of sources

**How to get it:**
1. Go to [NewsAPI](https://newsapi.org/)
2. Sign up for a free account
3. Copy your API key from the dashboard

**Cost:** Free tier includes 1,000 requests/day

### 4. 🧮 Wolfram Alpha API Key (Computational Intelligence)

**What it enables:** Mathematical calculations, scientific queries, data analysis

**How to get it:**
1. Go to [Wolfram Alpha Developer Portal](https://developer.wolframalpha.com/)
2. Sign up for an account
3. Create a new app
4. Copy the App ID

**Cost:** Free tier includes 2,000 queries/month

## 📝 Configuration Setup

1. **Open `advanced_config.json`** in your text editor

2. **Replace the placeholder values** with your actual API keys:

```json
{
  "openai_api_key": "sk-your-actual-openai-key-here",
  "weather_api_key": "your-openweathermap-key-here",
  "news_api_key": "your-newsapi-key-here",
  "wolfram_api_key": "your-wolfram-alpha-appid-here"
}
```

3. **Save the file** and restart Jarvis

## 📧 Email Configuration (Optional)

To enable email sending features:

1. **For Gmail users:**
   - Enable 2-factor authentication
   - Generate an "App Password" in your Google Account settings
   - Use the app password (not your regular password)

2. **Update config:**
```json
"email_settings": {
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "email": "your-email@gmail.com",
  "password": "your-app-password"
}
```

## 🔒 Security Best Practices

- **Never share your API keys** publicly
- **Keep your config file secure** and don't commit it to version control
- **Use environment variables** for production deployments
- **Monitor your API usage** to avoid unexpected charges

## 💡 Cost Optimization Tips

### OpenAI Usage:
- Use `gpt-3.5-turbo` instead of `gpt-4` for cost efficiency
- Keep conversation history reasonable (default: 10 messages)
- The assistant is designed to be cost-effective for daily use

### Expected Monthly Costs (Personal Use):
- **OpenAI:** $2-10 depending on usage
- **Weather API:** Free
- **News API:** Free
- **Wolfram Alpha:** Free
- **Total:** $2-10/month for full AI capabilities

## 🚀 Quick Start Commands

Once configured, try these advanced commands:

```
"Jarvis, what do you think about artificial intelligence?"
"Jarvis, weather in Tokyo"
"Jarvis, latest news about technology"
"Jarvis, calculate the square root of 144"
"Jarvis, what's the stock price of Apple?"
"Jarvis, remind me to call mom tomorrow"
```

## 🛠️ Troubleshooting

### Common Issues:

1. **"AI features disabled"**
   - Check your OpenAI API key is correct
   - Ensure you have credits in your OpenAI account

2. **"Weather service unavailable"**
   - Verify your OpenWeatherMap API key
   - Check if the city name is spelled correctly

3. **"News API not configured"**
   - Confirm your NewsAPI key is valid
   - Check your daily request limit

4. **API rate limits**
   - Most free tiers are generous for personal use
   - Consider upgrading if you hit limits

## 🎯 Next Steps

1. **Test each feature** to ensure APIs are working
2. **Customize personality** settings in the config
3. **Explore advanced commands** and AI conversations
4. **Set up email** for notification features
5. **Create custom commands** by modifying the code

Your Advanced Jarvis is now ready to provide intelligent, context-aware assistance with real-time information and AI-powered conversations! 🤖✨