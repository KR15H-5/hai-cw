# StateTracker keeps track of the current booking progress in the context
class StateTracker:
    # Return the current booking state, creating a fresh one if needed
    def get_state(self, context):
        if 'booking_state' not in context:
            context['booking_state'] = self.create_empty_state()
        return context['booking_state']
    
    # Apply updates to the booking state stored in the context
    def update_state(self, context, updates):
        if 'booking_state' not in context:
            context['booking_state'] = self.create_empty_state()
        context['booking_state'].update(updates)
    
    # Reset the booking state back to an empty template
    def reset_state(self, context):
        context['booking_state'] = self.create_empty_state()
    
    # Build a new empty booking state dictionary
    def create_empty_state(self):
        return {
            'stage': None,
            'movie': None,
            'time': None,
            'tickets': None,
            'seats': []
        }
    
    # Get the current stage name from the booking state
    def get_stage(self, context):
        state = self.get_state(context)
        return state.get('stage')
    
    # Set the current booking stage in the state
    def set_stage(self, context, stage):
        self.update_state(context, {'stage': stage})
    
    # Return True if a booking is currently in progress
    def is_in_booking(self, context):
        state = self.get_state(context)
        return state.get('stage') is not None
    
    # Return approximate booking progress as a percentage
    def get_progress(self, context):
        stages = ['time', 'tickets', 'seats', 'confirm']
        current_stage = self.get_stage(context)
        
        if not current_stage or current_stage not in stages:
            return 0
        
        current_idx = stages.index(current_stage)
        return int((current_idx + 1) / len(stages) * 100)

if __name__ == "__main__":
    pass
    # print("StateTracker module loaded successfully!")