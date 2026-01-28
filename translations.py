
MESSAGES = {
    "scab": {
        "ru": {
            "status": "Обнаружены признаки заболевания",
            "diagnosis": "Парша (визуальные признаки)",
            "symptom": "Темные, грубые, округлые поражения на поверхности листа.",
            "rec": "Визуальные симптомы обнаружены. Пожалуйста, проконсультируйтесь с агрономом для подтверждения диагноза."
        },
        "en": {
            "status": "Disease signs detected",
            "diagnosis": "Apple scab (visual signs)",
            "symptom": "Dark, rough, circular lesions on leaf surface.",
            "rec": "Visual symptoms detected. Please consult an agricultural specialist for confirmation."
        }
    },
    "rust": {
        "ru": {
            "status": "Обнаружены признаки заболевания",
            "diagnosis": "Ржавчина (визуальные признаки)",
            "symptom": "Оранжевые пустулы на нижней стороне листа.",
            "rec": "Визуальные симптомы обнаружены. Рекомендуется профессиональный осмотр для подтверждения."
        },
        "en": {
            "status": "Disease signs detected",
            "diagnosis": "Apple rust (visual signs)",
            "symptom": "Orange pustules forming on the underside of the leaf.",
            "rec": "Visual symptoms detected. Professional inspection is recommended for confirmation."
        }
    },
    "powdery_mildew": {
        "ru": {
            "status": "Обнаружены признаки заболевания",
            "diagnosis": "Мучнистая роса (визуальные признаки)",
            "symptom": "Белый порошкообразный налет на поверхности листа.",
            "rec": "Визуальные симптомы обнаружены. Для точной идентификации патогена обратитесь к специалисту."
        },
        "en": {
            "status": "Disease signs detected",
            "diagnosis": "Powdery Mildew (visual signs)",
            "symptom": "White powder-like coating on leaf surface.",
            "rec": "Visual symptoms detected. Contact a specialist for accurate pathogen identification."
        }
    },
    "frog_eye_leaf_spot": {
        "ru": {
            "status": "Обнаружены признаки заболевания",
            "diagnosis": "Пятнистость «лягушачий глаз»",
            "symptom": "Круглые коричневые пятна со светлым центром.",
            "rec": "Визуальные симптомы обнаружены. Требуется подтверждение специалиста перед принятием мер."
        },
        "en": {
            "status": "Disease signs detected",
            "diagnosis": "Frog-eye leaf spot (visual signs)",
            "symptom": "Circular brown spots with light centers.",
            "rec": "Visual symptoms detected. Specialist confirmation is required before taking action."
        }
    },
    "complex": {
        "ru": {
            "status": "Требуется внимание эксперта",
            "diagnosis": "Смешанные симптомы",
            "symptom": "Наблюдается несколько типов визуальных аномалий одновременно.",
            "rec": "Обнаружены признаки нескольких заболеваний. Рекомендуется срочный вызов специалиста для детальной оценки."
        },
        "en": {
            "status": "Expert attention required",
            "diagnosis": "Complex/Mixed symptoms",
            "symptom": "Multiple types of visual anomalies detected simultaneously.",
            "rec": "Signs of multiple diseases detected. Immediate expert consultation is recommended for detailed assessment."
        }
    },
    "healthy": {
        "ru": {
            "status": "Визуальных отклонений нет",
            "diagnosis": "Здоровый лист",
            "symptom": "Видимых симптомов болезней на поверхности листа не обнаружено.",
            "rec": "Лист выглядит здоровым. Продолжайте плановый мониторинг состояния сада."
        },
        "en": {
            "status": "No visual anomalies",
            "diagnosis": "Healthy leaf",
            "symptom": "No visible disease symptoms detected on the leaf surface.",
            "rec": "The leaf appears healthy. Continue regular monitoring of the orchard."
        }
    },
    # Запасной вариант для неопределенных случаев
    "unknown": {
        "ru": {
            "status": "Анализ затруднен",
            "diagnosis": "Не удалось определить",
            "symptom": "Изображение недостаточно четкое или объект не распознан.",
            "rec": "Попробуйте сделать фото при лучшем освещении или с другого ракурса."
        },
        "en": {
            "status": "Analysis difficult",
            "diagnosis": "Could not determine",
            "symptom": "The image is not clear enough or the object is not recognized.",
            "rec": "Try taking a photo with better lighting or from a different angle."
        }
    },

# --- Комбинированные результаты (Комбо) ---

    "scab frog_eye_leaf_spot": {
        "ru": {
            "status": "Обнаружено несколько заболеваний",
            "diagnosis": "Парша и Пятнистость (Frog-eye)",
            "symptom": "Сочетание темных грубых поражений и пятен со светлым центром.",
            "rec": "Выявлено смешанное поражение. Рекомендуется комплексная обработка фунгицидами."
        },
        "en": {
            "status": "Multiple diseases detected",
            "diagnosis": "Scab and Frog-eye leaf spot",
            "symptom": "Combination of dark rough lesions and spots with light centers.",
            "rec": "Mixed infection detected. Comprehensive fungicide treatment is recommended."
        }
    },

    "scab frog_eye_leaf_spot complex": {
        "ru": {
            "status": "Критическое состояние: множественные патогены",
            "diagnosis": "Парша, Пятнистость и сопутствующие инфекции",
            "symptom": "Массовое поражение листа различными типами пятен и налетов.",
            "rec": "Лист сильно поврежден несколькими болезнями. Срочно изолируйте пораженные ветви."
        },
        "en": {
            "status": "Critical: Multiple pathogens",
            "diagnosis": "Scab, Frog-eye, and Complex symptoms",
            "symptom": "Massive leaf damage with various types of spots and coatings.",
            "rec": "Leaf is severely damaged by multiple diseases. Urgently isolate affected branches."
        }
    },

    "rust frog_eye_leaf_spot": {
        "ru": {
            "status": "Обнаружено несколько заболеваний",
            "diagnosis": "Ржавчина и Пятнистость (Frog-eye)",
            "symptom": "Оранжевые пустулы в сочетании с коричневыми пятнами.",
            "rec": "Обнаружены признаки двух разных патогенов. Требуется подбор специфических препаратов."
        },
        "en": {
            "status": "Multiple diseases detected",
            "diagnosis": "Rust and Frog-eye leaf spot",
            "symptom": "Orange pustules combined with brown spots.",
            "rec": "Signs of two different pathogens detected. Specific drug selection required."
        }
    },

    "rust complex": {
        "ru": {
            "status": "Сложное инфекционное поражение",
            "diagnosis": "Ржавчина в сочетании с другими аномалиями",
            "symptom": "Характерные пустулы ржавчины на фоне общего угнетения тканей листа.",
            "rec": "Симптомы ржавчины осложнены другими факторами. Рекомендуется лабораторный анализ."
        },
        "en": {
            "status": "Complex infectious lesion",
            "diagnosis": "Rust with other anomalies",
            "symptom": "Characteristic rust pustules against a background of general leaf tissue degradation.",
            "rec": "Rust symptoms are complicated by other factors. Laboratory analysis is recommended."
        }
    },

    "frog_eye_leaf_spot complex": {
        "ru": {
            "status": "Прогрессирующее заболевание",
            "diagnosis": "Пятнистость «лягушачий глаз» (осложненная)",
            "symptom": "Множественные пятна со светлым центром, сливающиеся в общие зоны некроза.",
            "rec": "Болезнь переходит в тяжелую стадию. Необходима немедленная обработка сада."
        },
        "en": {
            "status": "Progressing disease",
            "diagnosis": "Frog-eye leaf spot (complicated)",
            "symptom": "Multiple light-centered spots merging into general areas of necrosis.",
            "rec": "Disease is moving into a severe stage. Immediate orchard treatment required."
        }
    },

    "powdery_mildew complex": {
        "ru": {
            "status": "Тяжелое грибковое поражение",
            "diagnosis": "Мучнистая роса в активной фазе",
            "symptom": "Плотный белый налет, сопровождающийся деформацией листа.",
            "rec": "Грибок активно распространяется. Удалите наиболее пораженные листья и проведите опрыскивание."
        },
        "en": {
            "status": "Severe fungal infection",
            "diagnosis": "Powdery Mildew (active phase)",
            "symptom": "Dense white coating accompanied by leaf deformation.",
            "rec": "Fungus is spreading actively. Remove most affected leaves and spray."
        }
    }
}

