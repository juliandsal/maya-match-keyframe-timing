# Maya Match Keyframe Timing

A PyMEL script for Autodesk Maya that allows you to bake target controls to match the timing of a reference control’s keyframes. This ensures consistent animation timing across multiple objects.

---

## Features

- Select a reference control and one or more target controls.  
- Bake target controls so their keyframes match the timing of the reference control.  
- Maintains the target controls’ animation values while aligning keyframe timing.  
- Provides a simple UI for selecting reference and target controls.  
- Ideal for stop-motion workflows, animation cleanup, or transferring timing across rigs.

---

## Installation

1. Place `MatchKeyframeTiming.py` in your Maya scripts folder.  
   - Windows: `Documents\maya\scripts\`  
   - macOS: `~/Library/Preferences/Autodesk/maya/scripts/`  
   - Linux: `~/maya/scripts/`

2. Start Maya and open the Script Editor.

3. Import the script:
```python
import MatchKeyframeTiming
