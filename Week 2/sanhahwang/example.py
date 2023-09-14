if __name__=='__main__':
    import logging, os, sys
    from gridenv import GridWorldEnv
    from datetime import datetime as dt
    import gymnasium as gym
    from gymnasium.utils.save_video import save_video

    # Folder name for the simulation
    FOLDER_NAME = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    os.makedirs(f"log/{FOLDER_NAME}")

    # Logger to have feedback on the console and on a file
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    logger = logging.getLogger(__name__)

    logger.info("-------------START-------------")

    obstacle_map = [
        "10001000",
        "10010000",
        "00000001",
        "01000001",
    ]
    
    env = GridWorldEnv(render_mode = "ansi")
    obs, info = env.reset(seed=1)
    Done = False
    reward = 0
    logger.info("Running action-perception loop...")
    
    with open(f"log/{FOLDER_NAME}/history.csv", 'w') as f:
        f.write(f"step,x,y,reward,done,action\n")
        
        for t in range(5000):
            #img = env.render(caption=f"t:{t}, rew:{rew}, pos:{obs}")
            
            action = env.action_space.sample()

            f.write(f"{t},{obs['agent'][0]},{obs['agent'][1]},{reward},{Done},{action}\n")
            

            if Done:
                logger.info(f"...agent is done at time step {t}")
                break
            
            obs, reward, terminated, Done, info = env.step(action)
            
    env.close()
    if env.render_mode == 'rgb_array':
        frames = env.render()
        save_video(frames, f"log/{FOLDER_NAME}", fps=env.fps)
    logger.info("...done")
    logger.info("-------------END-------------")