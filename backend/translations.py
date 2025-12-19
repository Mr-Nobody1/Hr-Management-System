"""
Translations - Multi-language support for the HR Management System.
"""
from typing import Dict, List


# Supported languages with their codes, names, and flags
SUPPORTED_LANGUAGES: List[Dict] = [
    {"code": "en", "name": "English", "native_name": "English", "flag": "🇬🇧", "rtl": False},
    {"code": "es", "name": "Spanish", "native_name": "Español", "flag": "🇪🇸", "rtl": False},
    {"code": "fr", "name": "French", "native_name": "Français", "flag": "🇫🇷", "rtl": False},
    {"code": "ar", "name": "Arabic", "native_name": "العربية", "flag": "🇸🇦", "rtl": True},
    {"code": "zh", "name": "Chinese", "native_name": "中文", "flag": "🇨🇳", "rtl": False},
]

# Language code to language info mapping
LANGUAGE_MAP: Dict[str, Dict] = {lang["code"]: lang for lang in SUPPORTED_LANGUAGES}


def get_language_instruction(language_code: str) -> str:
    """
    Get the LLM instruction for responding in a specific language.
    
    Args:
        language_code: ISO 639-1 language code (e.g., 'en', 'es', 'fr')
    
    Returns:
        Instruction string for the LLM
    """
    if language_code not in LANGUAGE_MAP:
        language_code = "en"  # Default to English
    
    lang = LANGUAGE_MAP[language_code]
    
    if language_code == "en":
        return ""  # No special instruction needed for English
    
    return f"""
IMPORTANT: Respond entirely in {lang['name']} ({lang['native_name']}). 
All text, headers, and explanations must be in {lang['name']}.
Only keep technical terms, names, and data values in English if necessary.
"""


def get_greeting(language_code: str, name: str = "there") -> str:
    """
    Get a greeting message in the specified language.
    
    Args:
        language_code: ISO 639-1 language code
        name: Name to greet
    
    Returns:
        Localized greeting string
    """
    greetings = {
        "en": f"Hello, {name}!",
        "es": f"¡Hola, {name}!",
        "fr": f"Bonjour, {name}!",
        "ar": f"!مرحبا، {name}",
        "zh": f"你好，{name}！",
    }
    return greetings.get(language_code, greetings["en"])


# Common UI translations for frontend fallback
UI_TRANSLATIONS = {
    "en": {
        "welcome": "Welcome to HR Assistant",
        "ask_anything": "Ask me anything about HR...",
        "send": "Send",
        "quick_actions": "Quick Actions",
        "agents_online": "Agents Online",
        "powered_by": "Powered by",
        "my_payslip": "My Payslip",
        "leave_balance": "Leave Balance",
        "my_profile": "My Profile",
        "clock_in": "Clock In",
        "my_benefits": "My Benefits",
        "my_team": "My Team",
        "performance": "Performance",
        "policies": "Policies",
        "select_language": "Select Language"
    },
    "es": {
        "welcome": "Bienvenido al Asistente de RRHH",
        "ask_anything": "Pregúntame sobre RRHH...",
        "send": "Enviar",
        "quick_actions": "Acciones Rápidas",
        "agents_online": "Agentes en Línea",
        "powered_by": "Desarrollado por",
        "my_payslip": "Mi Nómina",
        "leave_balance": "Saldo de Vacaciones",
        "my_profile": "Mi Perfil",
        "clock_in": "Registrar Entrada",
        "my_benefits": "Mis Beneficios",
        "my_team": "Mi Equipo",
        "performance": "Rendimiento",
        "policies": "Políticas",
        "select_language": "Seleccionar Idioma"
    },
    "fr": {
        "welcome": "Bienvenue à l'Assistant RH",
        "ask_anything": "Posez une question sur les RH...",
        "send": "Envoyer",
        "quick_actions": "Actions Rapides",
        "agents_online": "Agents en Ligne",
        "powered_by": "Propulsé par",
        "my_payslip": "Mon Bulletin",
        "leave_balance": "Solde de Congés",
        "my_profile": "Mon Profil",
        "clock_in": "Pointer",
        "my_benefits": "Mes Avantages",
        "my_team": "Mon Équipe",
        "performance": "Performance",
        "policies": "Politiques",
        "select_language": "Choisir la Langue"
    },
    "ar": {
        "welcome": "مرحبا بك في مساعد الموارد البشرية",
        "ask_anything": "اسألني عن الموارد البشرية...",
        "send": "إرسال",
        "quick_actions": "إجراءات سريعة",
        "agents_online": "الوكلاء متصلون",
        "powered_by": "مدعوم من",
        "my_payslip": "كشف راتبي",
        "leave_balance": "رصيد الإجازات",
        "my_profile": "ملفي الشخصي",
        "clock_in": "تسجيل الحضور",
        "my_benefits": "مزاياي",
        "my_team": "فريقي",
        "performance": "الأداء",
        "policies": "السياسات",
        "select_language": "اختر اللغة"
    },
    "zh": {
        "welcome": "欢迎使用人力资源助手",
        "ask_anything": "问我任何人力资源问题...",
        "send": "发送",
        "quick_actions": "快捷操作",
        "agents_online": "在线代理",
        "powered_by": "技术支持",
        "my_payslip": "我的工资单",
        "leave_balance": "休假余额",
        "my_profile": "我的资料",
        "clock_in": "打卡",
        "my_benefits": "我的福利",
        "my_team": "我的团队",
        "performance": "绩效",
        "policies": "政策",
        "select_language": "选择语言"
    }
}


def get_translation(language_code: str, key: str) -> str:
    """
    Get a translated UI string.
    
    Args:
        language_code: ISO 639-1 language code
        key: Translation key
    
    Returns:
        Translated string or English fallback
    """
    translations = UI_TRANSLATIONS.get(language_code, UI_TRANSLATIONS["en"])
    return translations.get(key, UI_TRANSLATIONS["en"].get(key, key))
