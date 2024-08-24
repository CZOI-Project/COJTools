from dataclasses import dataclass
from typing import List


@dataclass
class CheckpointToProblem:
    """CheckpointToProblem"""
    """提交给judger时附带信息，一般包含编译器参数等信息"""
    extra: str
    """测试点序号"""
    id: int
    """该测试点所用到的judger的id"""
    jid: str
    """内存限制，单位kb，注意，内存和时间限制需要与远程题目对应的一致。一般没什么用，仅供在页面呈现，或者看judger怎么处理"""
    memLimit: int
    """远程题目测试点编号"""
    nth: int
    """该测试点分数"""
    score: int
    """远程题目题号"""
    target: str
    """时间限制，单位ms"""
    timeLimit: int


@dataclass
class Subtask:
    """Subtask"""
    """包含的测试点"""
    checkpoints: List[CheckpointToProblem]
    """该子任务的分数"""
    score: int
    """计分方式，1：当前子任务的分数被测试点平分，确保能被整除，否则该子任务无法得到满分。在这种类型下，测试点自行设置的分数是无效的
    2：取当前子任务下得分最高的测试点的分数
    3：取当前子任务下得分最低的测试点的分数
    对于上述两种情况，子任务设置的分数是无效的
    4：单纯将测试点分数相加
    对于上述一种情况，子任务如果设置分数，则最后得分不会大于该数值
    特别地，如果该子任务的分数设置为0，则该子任务不参与计分

    题目的总分会根据上述规则进行计算
    注意，即使获得了满分，如果有一个测试点没有通过，那么该题目也会是unaccepted
    """
    type: int



