import json
from dataclasses import asdict

import click
import requests

import constants
import utils
from entity import Subtask, CheckpointToProblem


@click.group()
def cli():
    pass


@cli.group()
def cfg():
    pass  # 配置项


@cfg.command()
@click.argument("key")
@click.argument("value")
def put(key, value):
    try:
        with open("config.json", mode='r', encoding='utf-8') as file:
            all_data = json.load(file)
    except FileNotFoundError:
        all_data = {}
    all_data[key] = value
    with open("config.json", mode='w', encoding='utf-8') as file:
        json.dump(all_data, file)


@cli.group()
def chk():
    pass  # 测试点工具


@chk.command()
@click.argument("target")
def ls(target):
    # 查看测试点信息
    with open(f"{target}.json", mode='r', encoding='utf-8') as file:
        all_data = json.load(file)
    subtasks = [Subtask(**item) for item in all_data]
    for subtask in subtasks:
        subtask.checkpoints = [CheckpointToProblem(**item) for item in subtask.checkpoints]
    for index, subtask in enumerate(subtasks):
        if subtask.type == 1:
            click.echo(f"Subtask [{index}] 计分方式：{constants.subtask_type[subtask.type]} 总分：{subtask.score}")
        else:
            click.echo(f"Subtask [{index}] 计分方式：{constants.subtask_type[subtask.type]}")
        checkpoints = sorted(subtask.checkpoints, key=lambda x: x.id)
        for checkpoint in checkpoints:
            if subtask.type == 4:
                click.echo(f"\t[{checkpoint.id}] {checkpoint.jid}-{checkpoint.target}[{checkpoint.nth}] "
                           f"时限：{utils.get_time_text(checkpoint.timeLimit)} "
                           f"空限：{utils.get_mem_text(checkpoint.memLimit)} "
                           f"分数：{checkpoint.score}")
            else:
                click.echo(f"\t[{checkpoint.id}] {checkpoint.jid}-{checkpoint.target}[{checkpoint.nth}] "
                           f"时限：{utils.get_time_text(checkpoint.timeLimit)} "
                           f"空限：{utils.get_mem_text(checkpoint.memLimit)}")


@chk.group()
def delete():
    pass


@delete.command(name="point")
@click.argument("target", type=click.STRING)
@click.argument("subtask", type=click.INT)
@click.option("--start", '-s', type=click.INT, help="测试点编号起点", default=-1)
@click.option("--end", '-e', type=click.INT, help="测试点编号终点", default=-1)
def del_point(target, subtask, start, end):
    with open(f"{target}.json", mode='r', encoding='utf-8') as file:
        data = json.load(file)
    if start == -1:
        start = len(data[subtask]['checkpoints'])
    if end == -1:
        end = start
    ok = []
    for checkpoint in data[subtask]['checkpoints']:
        if checkpoint['id'] not in range(start, end + 1):
            ok.append(checkpoint)
    data[subtask]['checkpoints'] = ok
    with open(f"{target}.json", mode='w', encoding='utf-8') as file:
        json.dump(data, file)
    ls(target)


@chk.group()
def add():
    pass


@add.command(name="subtask")
@click.argument("target")
def add_subtask(target):
    with open(f"{target}.json", mode='r', encoding='utf-8') as file:
        all_data = json.load(file)
    all_data.append(asdict(Subtask([], 0, 0)))


@add.command(name="point")
@click.argument("target", type=click.STRING)
@click.argument("subtask", type=click.INT)
@click.option("--start", '-s', type=click.INT, help="测试点编号起点", default=-1)
@click.option("--end", '-e', type=click.INT, help="测试点编号终点", default=-1)
@click.option('--time', '-t', type=click.INT, help="时间限制", default=1000)
@click.option('--mem', '-m', type=click.INT, help="空间限制", default=524288)
@click.option('--jid', '-j', type=click.STRING, help="jid", default="")
@click.option('--remote', '-r', type=click.STRING, help="远程题目编号", default="")
@click.option('--nth', '-n', type=click.INT, help="对应远程题目的测试点编号，起始编号", default=0)
@click.option('--score', '-sc', type=click.INT, help="测试点分数", default=100)
def add_point(target, subtask, start, end, time, mem, jid, remote, nth, score):
    with open(f"{target}.json", mode='r', encoding='utf-8') as file:
        data = json.load(file)
    if start == -1:
        start = len(data[subtask]['checkpoints']) + 1
    if end == -1:
        end = start
    for i in range(start, end + 1):
        data[subtask]['checkpoints'].append(asdict(CheckpointToProblem(
            id=i,
            jid=jid,
            target=remote,
            nth=nth,
            score=score,
            extra="",
            memLimit=mem,
            timeLimit=time,
        )))
        nth += 1
    with open(f"{target}.json", mode='w', encoding='utf-8') as file:
        json.dump(data, file)
    ls(target)


@chk.command()
@click.argument("origin")
@click.argument("target")
@click.argument("name")
def fetch(origin, target, name):
    with open("config.json", mode='r', encoding='utf-8') as file:
        all_data = json.load(file)
    if origin == 'coj':
        if 'token' not in all_data:
            click.echo("没有设置token", err=True)
        token = all_data['token']
        res = requests.get(
            f"http://oi.caiwen.work/api/problem/subtask/detail?pid={target}",
            headers={"Authorization": token}
        )
        res = res.json()
        print(res)
        with open(f"{name}.json", mode='w', encoding='utf-8') as file:
            json.dump(res['data'], file)


if __name__ == '__main__':
    cli()
