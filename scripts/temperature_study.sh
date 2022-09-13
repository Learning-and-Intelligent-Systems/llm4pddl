FILE="llm4pddl/main.py"
NUM_TRAIN_TASKS="2"
SEEDS = (
    "0"
    "1"
    "2"
)
ENVS = (
    "gripper"
    "logistics"
    "miconic"
    "scanalyzer"
    "woodworking"
    "rovers"
    "parcprinter"
    "movie"
)
APPROACH = "llm-multi"
TEMPERATURES = (
    "0.0"
    "0.3"
    "0.5"
    "0.8"
    "0.9"
)
RESULTS_DIRS = (
    "results/0"
    "results/3"
    "results/5"
    "results/8"
    "results/9"
)
CACHE_DIRS = (
    "llm_cache/0"
    "llm_cache/3"
    "llm_cache/5"
    "llm_cache/8"
    "llm_cache/9"
)

for ENV in ${ENVS[@]}; do
    for SEED in ${SEEDS[@]}; do
        for TEMP in ${TEMPERATURES[@]}; do
            if [$TEMP = "0.0"]; then
                RESULT_DIR = "results/0"
                CACHE_DIR = "llm_cache/0"
            fi
            if [$TEMP = "0.3"]; then
                RESULT_DIR = "results/3"
                CACHE_DIR = "llm_cache/3"
            fi
            if [$TEMP = "0.5"]; then
                RESULT_DIR = "results/5"
                CACHE_DIR = "llm_cache/5"
            fi
            if [$TEMP = "0.8"]; then
                RESULT_DIR = "results/8"
                CACHE_DIR = "llm_cache/8"
            fi
            if [$TEMP = "0.9"]; then
                RESULT_DIR = "results/9"
                CACHE_DIR = "llm_cache/9"
            fi
            python $FILE --env pyperplan-${ENV} --approach $APPROACH --seed $SEED --data_gen_planner pyperplan --llm_multi_temperature $TEMP --results_dir $RESULT_DIR --llm_cache_dir $CACHE_DIR
        done
    done
done