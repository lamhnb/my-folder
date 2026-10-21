"""Build declared reduced viewing aids; native full PNGs remain evidence."""
from pathlib import Path
import cv2
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
for draw in range(1372,1377):
    cells=[]
    for cap in range(1,8):
        for sample in (0,1):
            folder=ROOT/'evidence'/'pilot_v1'/f'draw{draw:05d}_capture{cap:02d}'
            frame=cv2.imread(str(folder/f'frame_{sample:02d}.png'))
            # Excludes broadcast overlay; copied rail pixels are reduced only.
            im=cv2.resize(frame[220:840,:],(960,310),interpolation=cv2.INTER_AREA)
            cv2.putText(im,f'{draw} capture {cap} sample {sample}',(10,26),cv2.FONT_HERSHEY_SIMPLEX,.7,(0,255,255),2)
            cells.append(im)
    sheet=np.vstack([np.hstack(cells[i:i+2]) for i in range(0,len(cells),2)])
    cv2.imwrite(str(ROOT/'evidence'/f'readability_draw{draw:05d}.jpg'),sheet,[cv2.IMWRITE_JPEG_QUALITY,96])
