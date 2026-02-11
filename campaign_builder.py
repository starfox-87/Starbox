# Campaign Builder for Orchestrating Multi-Stage Adversary Attacks

class CampaignBuilder:
    def __init__(self):
        self.stages = []

    def add_stage(self, stage_name, actions):
        stage = {'name': stage_name, 'actions': actions}
        self.stages.append(stage)
        print(f"Stage '{stage_name}' added.")

    def orchestrate(self):
        for stage in self.stages:
            print(f"Executing stage: {stage['name']}")
            for action in stage['actions']:
                action.execute()  # Assuming each action has an execute() method

# Example action class for demonstration
class Action:
    def __init__(self, action_name):
        self.action_name = action_name
    
    def execute(self):
        print(f"Executing action: {self.action_name}")

# Example usage
if __name__ == '__main__':
    campaign = CampaignBuilder()
    campaign.add_stage('Initial Recon', [Action('Scan Network'), Action('Identify Vulnerabilities')])
    campaign.add_stage('Exploitation', [Action('Exploit Vulnerability')])
    campaign.orchestrate()