import random

def get_package_info(package_name, ecosystem='npm'):
    """Get package information"""
    
    # Mock data - in production, fetch from actual registry
    suspicious_patterns = []
    
    # Check for suspicious keywords
    suspicious_keywords = ['malicious', 'hack', 'exploit', 'backdoor', 'cryptominer', 'trojan']
    for keyword in suspicious_keywords:
        if keyword in package_name.lower():
            suspicious_patterns.append(f"Contains '{keyword}' in name")
    
    # Safe packages
    safe_packages = ['lodash', 'express', 'axios', 'react', 'vue', 'angular', 'django']
    
    return {
        'package_name': package_name,
        'ecosystem': ecosystem,
        'version': 'latest',
        'downloads': random.randint(1000, 10000000),
        'maintainers': random.randint(1, 10),
        'suspicious_patterns': suspicious_patterns,
        'is_known_safe': package_name.lower() in safe_packages
    }

def analyze_package_security(package_name, package_info):
    """Analyze package for security threats"""
    
    is_malicious = False
    severity = 'safe'
    confidence = 0.0
    alternatives = []
    
    # Check if package is known safe
    if package_info['is_known_safe']:
        is_malicious = False
        severity = 'safe'
        confidence = 0.95
        alternatives = []
    
    # Check for suspicious patterns
    elif package_info['suspicious_patterns']:
        is_malicious = True
        severity = 'high'
        confidence = 0.85
        alternatives = [
            f"safe-{package_name}",
            f"secure-{package_name}-alt",
            f"{package_name}-community"
        ]
    
    # Random check for unknown packages
    else:
        # In production, use AI/ML for analysis
        risk_score = random.random()
        if risk_score > 0.8:
            is_malicious = True
            severity = 'medium'
            confidence = 0.65
            alternatives = [f"trusted-{package_name}", f"{package_name}-core"]
        else:
            is_malicious = False
            severity = 'safe'
            confidence = 0.75
            alternatives = []
    
    return {
        'is_malicious': is_malicious,
        'severity': severity,
        'confidence': confidence,
        'alternatives': alternatives
    }