class StateTracker:
    """
    Tracks booking state machine
    Manages transitions between booking stages
    """
    
    def get_state(self, context):
        """Get current booking state"""
        if 'booking_state' not in context:
            context['booking_state'] = self.create_empty_state()
        return context['booking_state']
    
    def update_state(self, context, updates):
        """Update booking state"""
        if 'booking_state' not in context:
            context['booking_state'] = self.create_empty_state()
        context['booking_state'].update(updates)
    
    def reset_state(self, context):
        """Reset booking state to empty"""
        context['booking_state'] = self.create_empty_state()
    
    def create_empty_state(self):
        """Create an empty booking state"""
        return {
            'stage': None,
            'movie': None,
            'time': None,
            'tickets': None,
            'seats': []
        }
    
    def get_stage(self, context):
        """Get current booking stage"""
        state = self.get_state(context)
        return state.get('stage')
    
    def set_stage(self, context, stage):
        """Set booking stage"""
        self.update_state(context, {'stage': stage})
    
    def is_in_booking(self, context):
        """Check if user is currently in booking flow"""
        state = self.get_state(context)
        return state.get('stage') is not None
    
    def get_progress(self, context):
        """Get booking progress percentage"""
        stages = ['time', 'tickets', 'seats', 'confirm']
        current_stage = self.get_stage(context)
        
        if not current_stage or current_stage not in stages:
            return 0
        
        current_idx = stages.index(current_stage)
        return int((current_idx + 1) / len(stages) * 100)

if __name__ == "__main__":
    print("StateTracker module loaded successfully!")