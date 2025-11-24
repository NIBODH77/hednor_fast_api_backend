# # from pydantic_settings import BaseSettings
# # from typing import List

# # class Settings(BaseSettings):
# #     CORS_ORIGINS: List[str] = ["http://localhost:3000"]
# #     POSTGRES_USER: str = "postgres"
# #     POSTGRES_PASSWORD: str = "123456789"
# #     POSTGRES_SERVER: str = "localhost"
# #     POSTGRES_PORT: str = "5432"
# #     POSTGRES_DB: str = "hednor_db"
    
# #     @property
# #     def DATABASE_URL(self):
# #         return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
# #     class Config:
# #         env_file = ".env"
# #         env_file_encoding = 'utf-8'

# # settings = Settings()



# # from pydantic_settings import BaseSettings
# # from typing import List
# # from pydantic import BaseModel


# # class Settings(BaseSettings):
# #     CORS_ORIGINS: List[str] = ["http://localhost:3000"]
# #     POSTGRES_USER: str = "postgres"
# #     POSTGRES_PASSWORD: str = "123456789"
# #     POSTGRES_SERVER: str = "localhost"
# #     POSTGRES_PORT: str = "5432"
# #     POSTGRES_DB: str = "hednor_db"
    
# #     @property
# #     def DATABASE_URL(self):
# #         return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

# #     class Config:
# #         env_file = ".env"
# #         env_file_encoding = 'utf-8'

# #     # config.py
# # # from pathlib import Path

# # # BASE_DIR = Path(__file__).parent.parent
# # # IMAGE_UPLOAD_DIR = BASE_DIR / "uploads" / "products"

# # settings = Settings()










# from pydantic_settings import BaseSettings
# from typing import List
# from pathlib import Path
# from fastapi.middleware.cors import CORSMiddleware

# class Settings(BaseSettings):
#     CORS_ORIGINS: List[str] = ["http://localhost:3000"]
#     POSTGRES_USER: str = "postgres"
#     POSTGRES_PASSWORD: str = "123456789"
#     POSTGRES_SERVER: str = "localhost"
#     POSTGRES_PORT: str = "5432"
#     POSTGRES_DB: str = "hednor_db"
#     UPLOAD_DIR: str = "uploads"
    
#     @property
#     def DATABASE_URL(self):
#         return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

#     @property
#     def IMAGE_UPLOAD_DIR(self):
#         return Path(self.UPLOAD_DIR) / "products"

#     class Config:
#         env_file = ".env"
#         env_file_encoding = 'utf-8'
#         case_sensitive = False

# settings = Settings()



