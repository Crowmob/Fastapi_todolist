-- CreateTable
CREATE TABLE "Item" (
    "id" SERIAL NOT NULL,
    "item" TEXT NOT NULL,
    "checked" BOOLEAN NOT NULL,

    CONSTRAINT "Item_pkey" PRIMARY KEY ("id")
);
