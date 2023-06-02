### Src for Raspberry Pi 4B.

### Setup
1. Before Running code, Check Authority
    * Video Port
        ```
        sudo chmod 777 /dev/video0
        sudo usermod video roboin
        ```
    * Arduino Port
        ```    
        sudo chmod 777 /dev/ttyACM0
        ```
2. Run main.py for Actual Test
3. Run testing_conde.py for pre-calculated actions...
