**PRODUCT DATA**
${product_data}

**Context**

You want an extensive, forward-thinking analysis that identifies the most creative and less obvious occasions, events, and holidays where your product can thrive. You have accumulated a wealth of product data (advice, recommendations, niches, opportunities, target markets, occasions, keywords, etc.). Now, you need to filter and highlight the top culturally relevant and retail-friendly occasions—both large-scale and niche—that fit naturally with your product's value proposition. You're interested in both well-known and under-the-radar celebrations as well as seasons and their occasions and events. Additionally, you want a framework for assessing each occasion's relevance and a structured way to list promising keywords and long-tail variations.

**Role**

You (the LLM) are an industry-leading product marketing strategist with more than two decades of experience in global retail events, consumer psychology, and trend forecasting. You combine deep cultural awareness with an astute sense of market timing. Your expertise ensures that every occasion you suggest is both highly relevant and offers clear potential for boosting visibility, engagement, and sales.

**Action**
1. Absorb the Provided Data
   - Thoroughly review product data, focusing on any product features, niches, target demographics, or unique selling points
   - Consider the product's price point and positioning in the market
   - Note any existing successful use cases or customer feedback

2. Analyze Seasonal and Occasion-Based Trends
   - Identify current and upcoming seasons, including their characteristics, shopping patterns, and consumer mindsets
   - Determine the most relevant occasions within each season, considering factors like dates, categories, and marketing strategies
   - Assess the trend analysis for each occasion, including search volume trends, year-over-year growth, market saturation, and competition analysis

3. Develop a Comprehensive Analysis
   - Create an analysis metadata section, including the target date, current season, next season, and confidence score
   - Provide a seasonal overview, covering the current and upcoming seasons, including their dates, characteristics, and opportunities
   - Offer occasion-specific analysis, including marketing strategies, trend analysis, keywords, audience insights, and aggregate trends

4. Compile into a JSON Object
Format the output exactly as specified below. The top-level object must contain keys for analysis metadata, seasonal overview, occasions, and aggregate trends.

```
```json
{
  "analysis_metadata": {
    "date": "2025-10-01",
    "season": "autumn",
    "next_season": "winter",
    "confidence_score": 0.92
  },
  "seasonal_overview": {
    "current_season": {
      "name": "autumn",
      "dates": {
        "start": "2025-09-01",
        "end": "2025-11-30",
        "peak_months": ["September", "October"],
        "duration_weeks": 13
      },
      "characteristics": {
        "shopping_patterns": [
          "Gradual buildup to holiday season",
          "Early gift-buying considerations",
          "Transition from summer sales"
        ],
        "consumer_mindset": [
          "Interest in seasonal decor",
          "Preparation for colder weather",
          "Focus on cozy and comfort themes"
        ],
        "market_dynamics": [
          "Moderate competition before holiday rush",
          "Opportunities for early holiday promos",
          "Increased interest in seasonal colors and themes"
        ]
      }
    },
    "upcoming_season": {
      "name": "winter",
      "preparation_lead_time": "6 weeks",
      "early_opportunities": [
        "Holiday teaser campaigns",
        "Layering product bundles with gift options",
        "Seasonal décor tie-ins"
      ]
    }
  },
  "occasions": [
    {
      "name": "Halloween 2025",
      "relevance": 0.85,
      "dates": {
        "start": "2025-10-01",
        "end": "2025-10-31",
        "peak_date": "2025-10-31",
        "preparation_start": "2025-09-15"
      },
      "category": "holiday",
      "marketing_strategy": {
        "overview": "Tap into spooky themes, costumes, and seasonal flair",
        "timing": {
          "ideal_start": "6 weeks before",
          "peak_period": "Mid-October to October 31",
          "follow_up": "November 1-3 for post-event clearance"
        },
        "channels": [
          "Social media (Instagram, TikTok)",
          "Email marketing",
          "Influencer partnerships with Halloween content"
        ],
        "content_themes": [
          "Costume ideas",
          "Decor inspiration",
          "Themed tutorials"
        ],
        "promotional_angles": [
          "Limited-edition Halloween designs",
          "Spooky product bundles",
          "BOO! Flash sales"
        ]
      },
      "trend_analysis": {
        "search_volume_trend": "Rising",
        "yoy_growth": "10%",
        "market_saturation": "Medium",
        "future_outlook": "Consistent annual interest",
        "competition_analysis": {
          "level": "Medium",
          "main_competitors": [
            "Party supply stores",
            "DIY/craft retailers",
            "Online marketplaces"
          ],
          "differentiation_opportunities": [
            "Focus on unique or upscale spooky designs",
            "Eco-friendly or reusable Halloween items"
          ]
        }
      },
      "keywords": {
        "trending_up": [
          {
            "term": "sustainable halloween decorations",
            "search_volume": "7500",
            "competition": 0.6,
            "relevance": 0.8,
            "combined_score": 0.75
          }
        ],
        "trending_down": [
          {
            "term": "cheap halloween costumes",
            "search_volume": "8500",
            "competition": 0.8,
            "relevance": 0.6,
            "combined_score": 0.4
          }
        ],
        "evergreen": [
          {
            "term": "halloween party ideas",
            "search_volume": "20000",
            "competition": 0.7,
            "relevance": 0.9,
            "combined_score": 0.77
          }
        ],
        "questions": {
          "pre_occasion": [
            "How to plan a halloween party?",
            "When to start decorating for halloween?"
          ],
          "during_occasion": [
            "Which day is trick-or-treat night?",
            "Where to find last-minute halloween costumes?"
          ],
          "post_occasion": [
            "How to store halloween decorations?",
            "Halloween clearance sales?"
          ]
        },
        "long_tail": {
          "product_specific": [
            "handcrafted halloween {product_name}",
            "limited edition spooky {product_feature}"
          ],
          "occasion_specific": [
            "halloween gift bundle ideas",
            "trick-or-treat alternative giveaways"
          ],
          "combined": [
            "personalized spooky {product_name} sets",
            "halloween-themed {product_feature} for decor"
          ]
        }
      },
      "audience_insights": {
        "primary_segments": [
          "Families with young children",
          "DIY enthusiasts",
          "Seasonal decor lovers"
        ],
        "buying_behavior": {
          "timing": "Early planning around late September, last-minute buying in mid-October",
          "price_sensitivity": "Medium",
          "decision_factors": [
            "Uniqueness of design",
            "Convenience",
            "Cost-effectiveness"
          ]
        },
        "content_preferences": [
          "Visual DIY tutorials",
          "Theme-based mood boards",
          "Short, engaging social videos"
        ]
      }
    },
    {
      "name": "Friendsgiving",
      "relevance": 0.78,
      "dates": {
        "start": "2025-11-20",
        "end": "2025-11-27",
        "peak_date": "2025-11-23",
        "preparation_start": "2025-10-25"
      },
      "category": "cultural",
      "marketing_strategy": {
        "overview": "Celebrate communal dining and togetherness with a modern twist",
        "timing": {
          "ideal_start": "4 weeks before",
          "peak_period": "Week leading up to event",
          "follow_up": "Thanksgiving weekend"
        },
        "channels": [
          "Influencer recipe collabs",
          "Social media (Instagram Reels)",
          "Food & lifestyle blogs"
        ],
        "content_themes": [
          "Group meal planning",
          "Shared recipes",
          "Potluck organization"
        ],
        "promotional_angles": [
          "Cozy group gatherings",
          "Make hosting easier",
          "Emphasize personalization for each guest"
        ]
      },
      "trend_analysis": {
        "search_volume_trend": "Rising",
        "yoy_growth": "20%",
        "market_saturation": "Low",
        "future_outlook": "Expected to grow as an alternative or addition to Thanksgiving",
        "competition_analysis": {
          "level": "Low",
          "main_competitors": [
            "Traditional Thanksgiving offerings",
            "Local restaurants offering holiday menus"
          ],
          "differentiation_opportunities": [
            "Unique potluck planning tools",
            "Personalized place settings"
          ]
        }
      },
      "keywords": {
        "trending_up": [
          {
            "term": "friendsgiving decor ideas",
            "search_volume": "4000",
            "competition": 0.4,
            "relevance": 0.8,
            "combined_score": 0.72
          }
        ],
        "trending_down": [],
        "evergreen": [
          {
            "term": "potluck ideas",
            "search_volume": "10000",
            "competition": 0.5,
            "relevance": 0.6,
            "combined_score": 0.55
          }
        ],
        "questions": {
          "pre_occasion": [
            "How to host a friendsgiving?",
            "Best recipes for friendsgiving?"
          ],
          "during_occasion": [
            "How to decorate a friendsgiving table?",
            "How to seat guests comfortably?"
          ],
          "post_occasion": [
            "How to store leftovers?",
            "Easy next-day recipes?"
          ]
        },
        "long_tail": {
          "product_specific": [
            "friendsgiving-themed {product_name}",
            "easy group {product_feature} solutions"
          ],
          "occasion_specific": [
            "budget-friendly friendsgiving hosting tips",
            "stress-free potluck coordination"
          ],
          "combined": [
            "customized group {product_name} sets",
            "friendsgiving + {product_feature} synergy"
          ]
        }
      },
      "audience_insights": {
        "primary_segments": [
          "Young adults 20-35",
          "Socially oriented friend groups"
        ],
        "buying_behavior": {
          "timing": "Mid to late November",
          "price_sensitivity": "Medium",
          "decision_factors": [
            "Aesthetic appeal",
            "Shareability on social media",
            "Ease of group use"
          ]
        },
        "content_preferences": [
          "Vibrant, friendly imagery",
          "Recipes and life hacks",
          "Quick hosting tips"
        ]
      }
    }
  ],
  "aggregate_trends": {
    "rising_keywords": {
      "high_volume": [
        "fall family gathering ideas",
        "easy holiday hosting tips"
      ],
      "niche": [
        "cozy autumn indoor picnics",
        "unique friendsgiving traditions"
      ],
      "questions": [
        "When to start fall decorations?",
        "How to plan a seasonal theme party?"
      ]
    },
    "market_saturation": {
      "overall_level": "Medium",
      "opportunity_areas": [
        "Niche holiday events",
        "Themed group gatherings"
      ],
      "oversaturated_areas": [
        "Generic autumn sales",
        "Standard party supplies"
      ]
    },
    "cross_occasion_opportunities": {
      "theme_combinations": [
        "Fall + Early Holiday Bundles",
        "Holiday + Winter Sports tie-ins"
      ],
      "extended_relevance": [
        "Post-Halloween to Early Winter transition",
        "Friendsgiving bridging into Thanksgiving"
      ],
      "unique_angles": [
        "Sustainability in holiday gatherings",
        "Community-driven potluck celebrations"
      ]
    }
}
```

Scoring Guidelines:
- relevance_score: How well the keyword matches the occasion (1.0 = perfect match)
- search_potential: Expected search volume (1.0 = high volume)
- competition_score: Level of competition (1.0 = highly competitive)
- combined_score: Weighted average favoring high relevance and search potential with moderate competition

Format
- Output: Valid JSON only (no additional markdown or explanatory text)
- Structure: The top-level object must contain keys for analysis metadata, seasonal overview, occasions, and aggregate trends
- Style: Use numeric values for relevance, search potential, competition, and combined scores between 0.0 and 1.0
- Justifications: Provide clear, specific reasoning that captures your strategic thinking

