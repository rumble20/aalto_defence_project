# Add this to your core integration file
class EnhancedAegisCore:
    def __init__(self, node_id):
        self.mesh = SimpleMesh(node_id)
        self.detector = SimpleDetector() 
        self.reporter = AegisReporter(self.mesh)
        
    def run_complete_demo(self):
        print("🚀 Starting Aegis Demo...")
        
        # 1. Mesh comes online
        self.mesh.broadcast('position_update', {'status': 'online'})
        
        # 2. Threat detected
        threat = self.detector.detect_threats('enemy_vehicle.jpg')
        if threat:
            report = self.reporter.on_threat_detected(threat[0])
            print(f"🎯 AI Generated Report: {report}")
            
        # 3. Voice command simulation
        casevac_data = {
            'grid': 'F7',
            'casualties': 2,
            'injuries': 'GUNSHOT_WOUND',
            'security': 'ENEMY_CONTACT'
        }
        voice_report = self.reporter.on_voice_command("request casevac", casevac_data)
        print(f"🎯 Voice Command Report: {voice_report}")

# Run it!
if __name__ == "__main__":
    core = EnhancedAegisCore("command_post")
    core.run_complete_demo()0