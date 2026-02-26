## 2026-01-14 - Dynamic Widget Swapping in CustomTkinter
**Learning:** When dynamically changing widget visibility in `customtkinter` layouts using `pack(side='left')`, widgets must be explicitly unpacked and repacked in sequence to maintain the intended visual order. simply toggling visibility can alter the layout if other widgets are packed with the same alignment.
**Action:** When implementing similar dynamic UI changes, encapsulate the packing logic in a helper method or strictly control the sequence of `pack` calls.
