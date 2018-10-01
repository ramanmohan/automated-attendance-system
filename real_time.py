@author: Rajesh_Raman
import argparse
import sys
from tf_graph import FaceRecGraph
from align_custom import AlignCustom


from face_feature import FaceFeature
from face_recognition import face_Recognition

FRGraph = FaceRecGraph()
aligner = AlignCustom()
extract_feature = FaceFeature(FRGraph)

def main(args):
    mode = args.mode
    if(mode == "camera"):
        camera_recog()
    elif mode == "input":
        create_manual_data()
    elif mode == "embed":
        create_embedding()
    else:
        raise ValueError("Unimplemented mode")


def camera_recog():
    recognition = face_Recognition(FRGraph,aligner,extract_feature)
    recognition.recognize_Face()

def create_manual_data():
    create_database = face_Recognition(FRGraph,aligner,extract_feature)
    create_database.add_faces()

def create_embedding():
    create_embedding = face_Recognition(FRGraph,aligner,extract_feature)
    create_embedding.create_embeddings()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, help="Run camera recognition", default="camera")
    args = parser.parse_args(sys.argv[1:])
    main(args)
