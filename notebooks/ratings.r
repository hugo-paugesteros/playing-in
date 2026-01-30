# Install packages if you don't have them
# install.packages(c("ordinal", "emmeans"))

library(ordinal)
library(emmeans)

# 1. Load Data
df <- read.csv("../data/processed/ratings_blind.csv")

# 2. CRITICAL STEP: Define Data Types
# 'rating' must be an ORDERED factor (this tells R that 10 > 9 > 8)
df$rating <- as.ordered(as.factor(df$rating))

# 'player' must be a factor (for Random Effects)
df$player <- as.factor(df$player)

# 'violin' and 'session' are your Fixed Effects
df$violin <- as.factor(df$violin)
df$session <- as.factor(df$session) # Ensure these are labeled distinctively (e.g., "t0", "t1", "t2")
df$criterion <- as.factor(df$criterion)
df$scope <- as.factor(df$scope)

df_P <- subset(df, criterion == "T")
df_P <- droplevels(df_P)
df_P

df_control <- subset(df_P, scope == "control")

# Fit model
model_A <- clmm(rating ~ violin * session + (1|player), 
                data = df_control, 
                link = "logit")

# Check results (Pairwise comparison: t2 vs t0)
emm_A <- emmeans(model_A, ~ session | violin)
pairs(emm_A, reverse = TRUE)

# # Fit model on ALL data (Test + Control) for criterion P
# model_B <- clmm(rating ~ violin * session * scope + (1|player), 
#                 data = df_P, 
#                 link = "logit")

# # Check the specific contrast (Test vs Control change)
# emm_B <- emmeans(model_B, ~ session | violin | scope)
# # contrast(emm_B, interaction = "pairwise", by = "violin")
# custom_contrast <- list(
#   "T2_vs_Baseline" = c(-0.5, -0.5, 1) 
# )

# # 3. Apply it
# # This asks: "Is the difference (T2 - AvgBaseline) significant?"
# contrast(emm_B, method = custom_contrast, by = c("violin", "scope"))

# Filter for Test Player only
df_test <- subset(df_F, scope == "test")

# Use 'clm' (Standard Cumulative Link Model), NOT 'clmm' (Mixed Model)
# We remove +(1|player) because there is only 1 player.
model_test_simple <- clm(rating ~ violin * session, 
                         data = df_test, 
                         link = "logit")

# Test t2 vs Baseline
emm_test <- emmeans(model_A, ~ session | violin)
contrast(emm_test, method = list("T2_vs_Baseline" = c(-0.5, -0.5, 1)), by = "violin")