from sqlalchemy.orm import mapped_column, Mapped, declarative_base
from sqlalchemy import String, Integer, Numeric

BaseModel = declarative_base()


class Videojuego_rawg(BaseModel):

    __tablename__ = "videojuego_rawg"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    fecha_lanzamiento: Mapped[int] = mapped_column(Integer)
    imagen: Mapped[str] = mapped_column(String(250))
    valoracion: Mapped[float] = mapped_column(Numeric(10, 2))

    def __repr__(self) -> str:

        return f"Videojuego_rawg(id={self.id!r}, nombre={self.nombre!r}, fecha_lanzamiento={self.fecha_lanzamiento!r}, imagen={self.imagen!r}, valoracion={self.valoracion!r})"
